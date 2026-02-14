import os
import logging
import requests
from dotenv import load_dotenv
import json

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CloudflareDBManager:
    def __init__(self):
        """
        初始化 Cloudflare D1 数据库连接
        使用 Cloudflare API 访问 D1 数据库
        """
        try:
            self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
            self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
            self.database_id = os.getenv('CLOUDFLARE_D1_DATABASE_ID')
            
            if not all([self.account_id, self.api_token, self.database_id]):
                raise ValueError("缺少 Cloudflare 配置参数：CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, CLOUDFLARE_D1_DATABASE_ID")
            
            self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}"
            self.headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            logger.info("Cloudflare D1 database client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database client: {e}")
            raise
    
    def execute_sql(self, sql, params=None):
        """
        执行 SQL 查询
        :param sql: SQL 语句
        :param params: 参数列表
        :return: 查询结果
        """
        try:
            payload = {'sql': sql}
            if params:
                payload['params'] = params
            
            response = requests.post(
                f"{self.base_url}/query",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"SQL execution failed: {response.text}")
                return None
            
            result = response.json()
            if result.get('success'):
                return result.get('result', [])
            else:
                logger.error(f"SQL execution error: {result.get('errors', [])}")
                return None
                
        except Exception as e:
            logger.error(f"Error executing SQL: {e}")
            return None
    
    def insert_news(self, news_data):
        """
        插入新闻数据
        :param news_data: 新闻数据字典
        :return: 插入结果
        """
        try:
            sql = """
                INSERT INTO news_feed 
                (original_url, title_cn, title_id, thumbnail_r2_url, published_at, content_structure, is_crawled)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = [
                news_data.get('original_url', ''),
                news_data.get('title_cn', ''),
                news_data.get('title_id', ''),
                news_data.get('thumbnail_r2_url', ''),
                news_data.get('published_at', ''),
                json.dumps(news_data.get('content_structure', {})),
                news_data.get('is_crawled', False)
            ]
            
            result = self.execute_sql(sql, params)
            
            if result:
                logger.info(f"Inserted news: {news_data.get('title_id', '').strip()[:50]}...")
                return {'success': True, 'data': result}
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error inserting news: {e}")
            return None
    
    def get_news_by_date(self, date):
        """
        根据日期获取新闻
        :param date: 日期字符串 (YYYY-MM-DD)
        :return: 新闻列表
        """
        try:
            sql = """
                SELECT * FROM news_feed 
                WHERE published_at >= ? AND published_at <= ?
                ORDER BY published_at DESC
            """
            params = [f'{date} 00:00:00', f'{date} 23:59:59']
            
            result = self.execute_sql(sql, params)
            
            if result and len(result) > 0:
                return result[0].get('results', [])
            return []
            
        except Exception as e:
            logger.error(f"Error getting news by date: {e}")
            return []
    
    def get_all_news(self, limit=100):
        """
        获取所有新闻
        :param limit: 限制返回数量
        :return: 新闻列表
        """
        try:
            sql = f"SELECT * FROM news_feed ORDER BY published_at DESC LIMIT {limit}"
            result = self.execute_sql(sql)
            
            if result and len(result) > 0:
                return result[0].get('results', [])
            return []
            
        except Exception as e:
            logger.error(f"Error getting all news: {e}")
            return []
    
    def insert_vocabulary(self, vocab_data):
        """
        插入单词数据
        :param vocab_data: 单词数据字典
        :return: 插入结果
        """
        try:
            sql = """
                INSERT INTO vocabulary 
                (word_selected, meaning_cn, root_word, pos, vibe_check, context_sentence_id, source_article_id, is_archived)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = [
                vocab_data.get('word_selected', ''),
                vocab_data.get('meaning_cn', ''),
                vocab_data.get('root_word', ''),
                vocab_data.get('pos', ''),
                vocab_data.get('vibe_check', ''),
                vocab_data.get('context_sentence_id', ''),
                vocab_data.get('source_article_id'),
                vocab_data.get('is_archived', False)
            ]
            
            result = self.execute_sql(sql, params)
            
            if result:
                logger.info(f"Inserted vocabulary: {vocab_data.get('word_selected', '')}")
                return {'success': True, 'data': result}
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error inserting vocabulary: {e}")
            return None
    
    def get_vocabulary_by_date(self, date):
        """
        根据日期获取词汇表
        :param date: 日期字符串 (YYYY-MM-DD)
        :return: 词汇列表
        """
        try:
            sql = """
                SELECT * FROM vocabulary 
                WHERE created_at >= ? AND created_at <= ?
                ORDER BY created_at DESC
            """
            params = [f'{date} 00:00:00', f'{date} 23:59:59']
            
            result = self.execute_sql(sql, params)
            
            if result and len(result) > 0:
                return result[0].get('results', [])
            return []
            
        except Exception as e:
            logger.error(f"Error getting vocabulary by date: {e}")
            return []
    
    def insert_daily_digest(self, digest_data):
        """
        插入日报数据
        :param digest_data: 日报数据字典
        :return: 插入结果
        """
        try:
            sql = """
                INSERT INTO daily_digest 
                (date, digest_items)
                VALUES (?, ?)
            """
            params = [
                digest_data.get('date', ''),
                json.dumps(digest_data.get('digest_items', []))
            ]
            
            result = self.execute_sql(sql, params)
            
            if result:
                logger.info(f"Inserted daily digest for date: {digest_data.get('date')}")
                return {'success': True, 'data': result}
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error inserting daily digest: {e}")
            return None
    
    def get_daily_digest(self, date):
        """
        获取指定日期的日报
        :param date: 日期字符串 (YYYY-MM-DD)
        :return: 日报数据
        """
        try:
            sql = "SELECT * FROM daily_digest WHERE date = ?"
            params = [date]
            
            result = self.execute_sql(sql, params)
            
            if result and len(result) > 0:
                rows = result[0].get('results', [])
                if len(rows) > 0:
                    row = rows[0]
                    row['digest_items'] = json.loads(row.get('digest_items', '[]'))
                    return row
            return None
            
        except Exception as e:
            logger.error(f"Error getting daily digest: {e}")
            return None
    
    def update_news(self, news_id, update_data):
        """
        更新新闻数据
        :param news_id: 新闻 ID
        :param update_data: 更新数据字典
        :return: 更新结果
        """
        try:
            set_clauses = []
            params = []
            
            for key, value in update_data.items():
                if key == 'content_structure':
                    set_clauses.append(f"{key} = ?")
                    params.append(json.dumps(value))
                else:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            params.append(news_id)
            
            sql = f"UPDATE news_feed SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            
            result = self.execute_sql(sql, params)
            
            if result:
                logger.info(f"Updated news: {news_id}")
                return {'success': True, 'data': result}
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error updating news: {e}")
            return None
    
    def delete_news(self, news_id):
        """
        删除新闻
        :param news_id: 新闻 ID
        :return: 删除结果
        """
        try:
            sql = "DELETE FROM news_feed WHERE id = ?"
            params = [news_id]
            
            result = self.execute_sql(sql, params)
            
            if result:
                logger.info(f"Deleted news: {news_id}")
                return {'success': True, 'data': result}
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error deleting news: {e}")
            return None

if __name__ == "__main__":
    try:
        db_manager = CloudflareDBManager()
        logger.info("Database manager initialized successfully")
        
        # 测试查询
        news_list = db_manager.get_all_news(limit=10)
        logger.info(f"Got {len(news_list)} news items")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
