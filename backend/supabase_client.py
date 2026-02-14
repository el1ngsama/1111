import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# 加载环境变量
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        """
        初始化 Supabase 客户端
        """
        try:
            self.url = os.getenv('SUPABASE_URL')
            self.key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if not all([self.url, self.key]):
                raise ValueError("缺少 Supabase 配置参数")
            
            # 创建 Supabase 客户端
            self.supabase: Client = create_client(self.url, self.key)
            logger.info("Supabase client initialized successfully")
            
            # 暂时跳过表初始化，避免启动时的错误
            # self.init_tables()
            
        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")
            raise
    def init_tables(self):
        """
        初始化数据库表结构
        """
        try:
            # 创建 news_feed 表
            self.create_news_feed_table()
            
            # 创建 vocabulary 表
            self.create_vocabulary_table()
            
            # 创建 daily_digest 表
            self.create_daily_digest_table()
            
        except Exception as e:
            logger.error(f"Error initializing tables: {e}")
            raise
    def create_news_feed_table(self):
        """
        创建 news_feed 表
        """
        try:
            # 检查表是否存在
            result = self.supabase.rpc('table_exists', {'table_name': 'news_feed'}).execute()
            table_exists = result.data if result.data is not None else False
            
            if not table_exists:
                # 创建表
                query = """
                CREATE TABLE IF NOT EXISTS news_feed (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    original_url TEXT UNIQUE NOT NULL,
                    title_cn TEXT,
                    title_id TEXT NOT NULL,
                    thumbnail_r2_url TEXT,
                    published_at TIMESTAMP WITH TIME ZONE,
                    content_structure JSONB,
                    is_crawled BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                -- 创建索引
                CREATE INDEX IF NOT EXISTS idx_news_feed_published_at ON news_feed(published_at DESC);
                CREATE INDEX IF NOT EXISTS idx_news_feed_is_crawled ON news_feed(is_crawled);
                """
                
                self.supabase.sql(query).execute()
                logger.info("Created news_feed table")
            else:
                logger.info("news_feed table already exists")
                
        except Exception as e:
            logger.error(f"Error creating news_feed table: {e}")
            raise
    def create_vocabulary_table(self):
        """
        创建 vocabulary 表
        """
        try:
            # 检查表是否存在
            result = self.supabase.rpc('table_exists', {'table_name': 'vocabulary'}).execute()
            table_exists = result.data if result.data is not None else False
            
            if not table_exists:
                # 创建表
                query = """
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    word_selected TEXT NOT NULL,
                    meaning_cn TEXT,
                    root_word TEXT,
                    pos TEXT,
                    vibe_check TEXT,
                    context_sentence_id TEXT,
                    source_article_id UUID REFERENCES news_feed(id),
                    is_archived BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                -- 创建索引
                CREATE INDEX IF NOT EXISTS idx_vocabulary_word_selected ON vocabulary(word_selected);
                CREATE INDEX IF NOT EXISTS idx_vocabulary_is_archived ON vocabulary(is_archived);
                """
                
                self.supabase.sql(query).execute()
                logger.info("Created vocabulary table")
            else:
                logger.info("vocabulary table already exists")
                
        except Exception as e:
            logger.error(f"Error creating vocabulary table: {e}")
            raise
    def create_daily_digest_table(self):
        """
        创建 daily_digest 表
        """
        try:
            # 检查表是否存在
            result = self.supabase.rpc('table_exists', {'table_name': 'daily_digest'}).execute()
            table_exists = result.data if result.data is not None else False
            
            if not table_exists:
                # 创建表
                query = """
                CREATE TABLE IF NOT EXISTS daily_digest (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    date DATE UNIQUE NOT NULL,
                    digest_items JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                -- 创建索引
                CREATE INDEX IF NOT EXISTS idx_daily_digest_date ON daily_digest(date DESC);
                """
                
                self.supabase.sql(query).execute()
                logger.info("Created daily_digest table")
            else:
                logger.info("daily_digest table already exists")
                
        except Exception as e:
            logger.error(f"Error creating daily_digest table: {e}")
            raise
    def insert_news(self, news_data):
        """
        插入新闻数据
        :param news_data: 新闻数据
        :return: 插入结果
        """
        try:
            result = self.supabase.table('news_feed').insert(news_data).execute()
            logger.info(f"Inserted news: {news_data.get('title_id', '').strip()[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error inserting news: {e}")
            return None
    def get_news_by_date(self, date):
        """
        根据日期获取新闻
        :param date: 日期
        :return: 新闻列表
        """
        try:
            result = self.supabase.table('news_feed').select('*').gte('published_at', f'{date} 00:00:00').lte('published_at', f'{date} 23:59:59').order('published_at', desc=True).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error getting news by date: {e}")
            return []
    def insert_vocabulary(self, vocab_data):
        """
        插入单词数据
        :param vocab_data: 单词数据
        :return: 插入结果
        """
        try:
            result = self.supabase.table('vocabulary').insert(vocab_data).execute()
            logger.info(f"Inserted vocabulary: {vocab_data.get('word_selected', '')}")
            return result
            
        except Exception as e:
            logger.error(f"Error inserting vocabulary: {e}")
            return None
    def insert_daily_digest(self, digest_data):
        """
        插入日报数据
        :param digest_data: 日报数据
        :return: 插入结果
        """
        try:
            result = self.supabase.table('daily_digest').insert(digest_data).execute()
            logger.info(f"Inserted daily digest for date: {digest_data.get('date')}")
            return result
            
        except Exception as e:
            logger.error(f"Error inserting daily digest: {e}")
            return None
    def get_daily_digest(self, date):
        """
        获取指定日期的日报
        :param date: 日期
        :return: 日报数据
        """
        try:
            result = self.supabase.table('daily_digest').select('*').eq('date', date).execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting daily digest: {e}")
            return None

if __name__ == "__main__":
    # 测试 Supabase 客户端
    try:
        supabase_manager = SupabaseManager()
        logger.info("Supabase manager initialized successfully")
        
        # 测试插入新闻
        test_news = {
            'original_url': 'https://www.detik.com/test',
            'title_id': 'Test news title',
            'title_cn': '测试新闻标题',
            'thumbnail_r2_url': 'https://example.com/test.jpg',
            'published_at': '2024-01-01T12:00:00Z',
            'is_crawled': True
        }
        
        result = supabase_manager.insert_news(test_news)
        logger.info(f"Insert news result: {result}")
        
        # 测试获取新闻
        news_list = supabase_manager.get_news_by_date('2024-01-01')
        logger.info(f"Got {len(news_list)} news items")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")