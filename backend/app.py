from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import DetikCrawler
# from r2_storage import R2Storage  # 暂时禁用R2存储
from deepseek_client import DeepSeekClient
from sqlite_db import SQLiteDBManager
import os
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化爬虫
crawler = DetikCrawler()

# 初始化 R2 存储（暂时禁用）
# r2_storage = None
# try:
#     r2_storage = R2Storage()
#     logger.info("R2 storage initialized successfully")
# except Exception as e:
#     logger.warning(f"R2 storage initialization failed: {e}")
#     logger.warning("Image processing will be skipped")

# 初始化 DeepSeek 客户端
deepseek_client = None
try:
    deepseek_client = DeepSeekClient()
    logger.info("DeepSeek client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing DeepSeek client: {e}")
    logger.warning("Translation and word analysis will be skipped")

# 初始化 SQLite 数据库管理器
db_manager = None
try:
    db_manager = SQLiteDBManager()
    logger.info("SQLite database manager initialized successfully")
except Exception as e:
    logger.warning(f"SQLite database manager initialization failed: {e}")
    logger.warning("Database operations will be skipped")

@app.route('/api/news', methods=['GET'])
def get_news():
    """
    获取新闻列表
    支持参数：date (YYYY-MM-DD)，默认为昨天
    """
    try:
        date = request.args.get('date')
        
        if not date:
            # 默认为昨天
            from datetime import datetime, timedelta
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 优先从数据库获取
        news_list = []
        if db_manager:
            news_list = db_manager.get_news_by_date(date)
            logger.info(f"Got {len(news_list)} news items from database")
        
        # 如果数据库中没有，从 detik.com 抓取
        if not news_list:
            news_list = crawler.get_news_list(date)
            
            # 处理图片上传到 R2（暂时禁用）
            # if r2_storage:
            #     processed_news_list = []
            #     for news in news_list:
            #         try:
            #             if news.get('image_url'):
            #                 # 处理封面图
            #                 r2_image_url = r2_storage.process_image(news['image_url'], f"news/{date}")
            #                 if r2_image_url:
            #                     news['image_url'] = r2_image_url
            #         except Exception as e:
            #             logger.error(f"Error processing news image: {e}")
            #             processed_news_list.append(news)
            #     news_list = processed_news_list
            
            # 翻译新闻标题（优化：只翻译前10条，避免超时）
            if deepseek_client:
                try:
                    # 只翻译前10条新闻，避免响应超时
                    news_to_translate = news_list[:10]
                    translated_news = deepseek_client.translate_news(news_to_translate)
                    
                    # 将翻译结果合并回原列表
                    for i, news in enumerate(news_list):
                        if i < len(translated_news):
                            news['title_cn'] = translated_news[i].get('title_cn', news.get('title', ''))
                        else:
                            news['title_cn'] = news.get('title', '')
                except Exception as e:
                    logger.error(f"Error translating news list: {e}")
                    # 翻译失败时，仍然返回原始数据
                    for news in news_list:
                        if 'title_cn' not in news:
                            news['title_cn'] = news.get('title', '')
            else:
                # 如果没有DeepSeek客户端，使用原标题
                for news in news_list:
                    if 'title_cn' not in news:
                        news['title_cn'] = news.get('title', '')
            
            # 存储到数据库
            if db_manager:
                for news in news_list:
                    news_data = {
                        'original_url': news.get('url', ''),
                        'title_id': news.get('title', ''),
                        'title_cn': news.get('title_cn', ''),
                        'thumbnail_r2_url': news.get('image_url', ''),
                        'published_at': news.get('published_at', ''),
                        'is_crawled': False
                    }
                    db_manager.insert_news(news_data)
            
        return jsonify({
            'success': True,
            'data': news_list,
            'message': f'获取 {date} 的新闻列表成功'
        })
        
    except Exception as e:
        logger.error(f"Error in get_news: {e}")
        return jsonify({
            'success': False,
            'message': f'获取新闻列表失败: {str(e)}'
        }), 500

@app.route('/api/article', methods=['GET'])
def get_article():
    """
    获取文章详情
    支持参数：url（文章链接）
    """
    try:
        url = request.args.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'message': '缺少文章链接参数'
            }), 400
        
        article_detail = crawler.get_article_detail(url)
        
        # 处理图片上传到 R2（暂时禁用）
        # if r2_storage:
        #     if article_detail.get('images'):
        #         processed_images = []
        #         for image_url in article_detail['images']:
        #             try:
        #                 r2_image_url = r2_storage.process_image(image_url, "articles")
        #                 if r2_image_url:
        #                     processed_images.append(r2_image_url)
        #                 else:
        #                     processed_images.append(image_url)
        #             except Exception as e:
        #                 logger.error(f"Error processing article image: {e}")
        #                 processed_images.append(image_url)
        #         article_detail['images'] = processed_images
        
        # 翻译文章内容
        if deepseek_client:
            try:
                article_detail = deepseek_client.translate_article(article_detail)
            except Exception as e:
                logger.error(f"Error translating article: {e}")
        
        return jsonify({
            'success': True,
            'data': article_detail,
            'message': '获取文章详情成功'
        })
        
    except Exception as e:
        logger.error(f"Error in get_article: {e}")
        return jsonify({
            'success': False,
            'message': f'获取文章详情失败: {str(e)}'
        }), 500

@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary():
    """
    获取每日词汇表
    支持参数：date (YYYY-MM-DD)，默认为今天
    """
    try:
        date = request.args.get('date')
        
        if not date:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 从数据库获取每日词汇表
        vocab_data = None
        if db_manager:
            existing_digest = db_manager.get_daily_digest(date)
            if existing_digest:
                vocab_data = existing_digest.get('digest_items', [])
            else:
                vocab_data = db_manager.get_vocabulary_by_date(date)
                # 创建日报
                digest_data = {
                    'date': date,
                    'digest_items': vocab_data
                }
                db_manager.insert_daily_digest(digest_data)
        
        return jsonify({
            'success': True,
            'data': vocab_data if vocab_data else [],
            'message': f'获取 {date} 的词汇表成功'
        })
        
    except Exception as e:
        logger.error(f"Error in get_vocabulary: {e}")
        return jsonify({
            'success': False,
            'message': f'获取词汇表失败: {str(e)}'
        }), 500

@app.route('/api/word', methods=['GET'])
def get_word():
    """
    查询单词信息
    支持参数：word（单词）
    """
    try:
        word = request.args.get('word')
        
        if not word:
            return jsonify({
                'success': False,
                'message': '缺少单词参数'
            }), 400
        
        # 使用 DeepSeek 分析单词（暂时禁用）
        # word_data = None
        # if deepseek_client:
        #     word_data = deepseek_client.analyze_word(word)
        
        return jsonify({
            'success': True,
            'data': word_data if word_data else {
                'word': word,
                'meaning': 'DeepSeek翻译功能暂时禁用',
                'examples': []
            },
            'message': f'查询单词 {word} 成功'
        })
        
    except Exception as e:
        logger.error(f"Error in get_word: {e}")
        return jsonify({
            'success': False,
            'message': f'查询单词失败: {str(e)}'
        }), 500

@app.route('/api/analyze/word', methods=['POST'])
def analyze_word():
    """
    分析单词
    支持参数：word（单词），context（上下文）
    """
    try:
        data = request.get_json()
        word = data.get('word')
        context = data.get('context', '')
        
        if not word:
            return jsonify({
                'success': False,
                'message': '缺少单词参数'
            }), 400
        
        # 使用 DeepSeek 分析单词
        word_data = None
        if deepseek_client:
            word_data = deepseek_client.analyze_word(word, context)
        
        if word_data:
            return jsonify({
                'success': True,
                'data': word_data,
                'message': f'分析单词 {word} 成功'
            })
        else:
            # 如果 DeepSeek 分析失败，返回模拟数据
            return jsonify({
                'success': True,
                'data': {
                    'word': word,
                    'meaning_cn': '示例翻译：这是一个示例单词的中文释义',
                    'root_word': '示例词根',
                    'pos': '名词',
                    'vibe_check': '正式用语，常用于新闻报道',
                    'context_sentence_id': context or '这是包含该单词的完整原句示例'
                },
                'message': f'分析单词 {word} 成功（使用模拟数据）'
            })
        
    except Exception as e:
        logger.error(f"Error in analyze_word: {e}")
        return jsonify({
            'success': False,
            'message': f'分析单词失败: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    return jsonify({
        'success': True,
        'message': '服务正常运行',
        'timestamp': 'now()'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)