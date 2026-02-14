import os
import requests
from io import BytesIO
from minio import Minio
from minio.error import S3Error
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class R2Storage:
    def __init__(self):
        """
        初始化 Cloudflare R2 客户端
        """
        try:
            self.endpoint = os.getenv('R2_ENDPOINT')
            self.access_key = os.getenv('R2_ACCESS_KEY')
            self.secret_key = os.getenv('R2_SECRET_KEY')
            self.bucket_name = os.getenv('R2_BUCKET_NAME')
            self.public_url = os.getenv('R2_PUBLIC_URL')
            
            if not all([self.endpoint, self.access_key, self.secret_key, self.bucket_name]):
                raise ValueError("缺少 R2 配置参数")
            
            # 初始化 MinIO 客户端（Cloudflare R2 兼容 S3 API）
            self.client = Minio(
                endpoint=self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=True
            )
            
            # 检查桶是否存在，不存在则创建
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            else:
                logger.info(f"Bucket {self.bucket_name} already exists")
                
        except Exception as e:
            logger.error(f"Error initializing R2 client: {e}")
            raise
    def download_image(self, image_url):
        """
        下载图片
        :param image_url: 图片 URL
        :return: 图片二进制数据
        """
        try:
            logger.info(f"Downloading image from: {image_url}")
            
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            return BytesIO(response.content)
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None
    def upload_image(self, image_data, object_name):
        """
        上传图片到 R2
        :param image_data: 图片二进制数据
        :param object_name: 对象名称
        :return: R2 访问 URL
        """
        try:
            if not image_data:
                return None
            
            # 重置文件指针到开头
            image_data.seek(0)
            
            # 获取文件大小
            image_size = len(image_data.getvalue())
            
            # 上传文件
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=image_data,
                length=image_size,
                content_type='image/jpeg'
            )
            
            # 生成访问 URL
            if self.public_url:
                r2_url = f"{self.public_url}/{object_name}"
            else:
                # 如果没有配置公共 URL，则使用 R2 提供的 URL 格式
                r2_url = f"https://{self.bucket_name}.{self.endpoint}/{object_name}"
            
            logger.info(f"Uploaded image to R2: {r2_url}")
            return r2_url
            
        except S3Error as e:
            logger.error(f"S3 error uploading image: {e}")
            return None
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None
    def process_image(self, image_url, object_prefix):
        """
        处理图片：下载并上传到 R2
        :param image_url: 原始图片 URL
        :param object_prefix: 对象前缀（用于生成唯一的对象名称）
        :return: R2 访问 URL
        """
        try:
            if not image_url:
                return None
            
            # 下载图片
            image_data = self.download_image(image_url)
            if not image_data:
                return None
            
            # 生成唯一的对象名称
            import uuid
            import os
            
            # 获取文件扩展名
            ext = os.path.splitext(image_url)[1] or '.jpg'
            object_name = f"{object_prefix}/{uuid.uuid4()}{ext}"
            
            # 上传到 R2
            r2_url = self.upload_image(image_data, object_name)
            return r2_url
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return None

if __name__ == "__main__":
    # 测试 R2 存储功能
    try:
        r2 = R2Storage()
        
        # 测试图片 URL
        test_image_url = "https://example.com/test.jpg"
        
        # 处理图片
        r2_url = r2.process_image(test_image_url, "test")
        print(f"R2 URL: {r2_url}")
        
    except Exception as e:
        print(f"Test failed: {e}")