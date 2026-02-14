import os
import logging
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SQLiteDBManager:
    def __init__(self, db_path='news_data.db'):
        """
        初始化 SQLite 数据库连接
        :param db_path: 数据库文件路径
        """
        try:
            self.db_path = db_path
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            
            # 初始化数据库表
            self.init_tables()
            
            logger.info("SQLite database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def init_tables(self):
        """
        初始化数据库表结构
        """
        try:
            # 创建 news_feed 表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS news_feed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT UNIQUE NOT NULL,
                    title_cn TEXT,
                    title_id TEXT NOT NULL,
                    thumbnail_r2_url TEXT,
                    published_at TIMESTAMP,
                    content_structure TEXT,
                    is_crawled BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建 vocabulary 表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_selected TEXT NOT NULL,
                    meaning_cn TEXT,
                    root_word TEXT,
                    pos TEXT,
                    vibe_check TEXT,
                    context_sentence_id TEXT,
                    source_article_id INTEGER,
                    is_archived BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建 daily_digest 表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_digest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE NOT NULL,
                    digest_items TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_feed_published_at ON news_feed(published_at DESC)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_feed_is_crawled ON news_feed(is_crawled)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_vocabulary_word_selected ON vocabulary(word_selected)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_vocabulary_is_archived ON vocabulary(is_archived)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_digest_date ON daily_digest(date DESC)')
            
            self.conn.commit()
            logger.info("Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing tables: {e}")
            raise
    
    def insert_news(self, news_data):
        """
        插入新闻数据
        :param news_data: 新闻数据字典
        :return: 插入结果
        """
        try:
            sql = '''
                INSERT OR REPLACE INTO news_feed 
                (original_url, title_cn, title_id, thumbnail_r2_url, published_at, content_structure, is_crawled)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                news_data.get('original_url', ''),
                news_data.get('title_cn', ''),
                news_data.get('title_id', ''),
                news_data.get('thumbnail_r2_url', ''),
                news_data.get('published_at', ''),
                json.dumps(news_data.get('content_structure', {})),
                1 if news_data.get('is_crawled', False) else 0
            )
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            
            logger.info(f"Inserted news: {news_data.get('title_id', '').strip()[:50]}...")
            return {'success': True, 'data': {'id': self.cursor.lastrowid}}
            
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
            sql = '''
                SELECT * FROM news_feed 
                WHERE published_at >= ? AND published_at <= ?
                ORDER BY published_at DESC
            '''
            params = [f'{date} 00:00:00', f'{date} 23:59:59']
            
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                news_dict = dict(row)
                if news_dict.get('content_structure'):
                    news_dict['content_structure'] = json.loads(news_dict['content_structure'])
                result.append(news_dict)
            
            return result
            
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
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                news_dict = dict(row)
                if news_dict.get('content_structure'):
                    news_dict['content_structure'] = json.loads(news_dict['content_structure'])
                result.append(news_dict)
            
            return result
            
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
            sql = '''
                INSERT INTO vocabulary 
                (word_selected, meaning_cn, root_word, pos, vibe_check, context_sentence_id, source_article_id, is_archived)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                vocab_data.get('word_selected', ''),
                vocab_data.get('meaning_cn', ''),
                vocab_data.get('root_word', ''),
                vocab_data.get('pos', ''),
                vocab_data.get('vibe_check', ''),
                vocab_data.get('context_sentence_id', ''),
                vocab_data.get('source_article_id'),
                1 if vocab_data.get('is_archived', False) else 0
            )
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            
            logger.info(f"Inserted vocabulary: {vocab_data.get('word_selected', '')}")
            return {'success': True, 'data': {'id': self.cursor.lastrowid}}
            
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
            sql = '''
                SELECT * FROM vocabulary 
                WHERE created_at >= ? AND created_at <= ?
                ORDER BY created_at DESC
            '''
            params = [f'{date} 00:00:00', f'{date} 23:59:59']
            
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            return [dict(row) for row in rows]
            
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
            sql = '''
                INSERT OR REPLACE INTO daily_digest 
                (date, digest_items)
                VALUES (?, ?)
            '''
            params = (
                digest_data.get('date', ''),
                json.dumps(digest_data.get('digest_items', []))
            )
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            
            logger.info(f"Inserted daily digest for date: {digest_data.get('date')}")
            return {'success': True, 'data': {'id': self.cursor.lastrowid}}
            
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
            
            self.cursor.execute(sql, params)
            row = self.cursor.fetchone()
            
            if row:
                digest_dict = dict(row)
                if digest_dict.get('digest_items'):
                    digest_dict['digest_items'] = json.loads(digest_dict['digest_items'])
                return digest_dict
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
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            
            logger.info(f"Updated news: {news_id}")
            return {'success': True, 'data': {'id': news_id}}
            
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
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            
            logger.info(f"Deleted news: {news_id}")
            return {'success': True, 'data': {'id': news_id}}
            
        except Exception as e:
            logger.error(f"Error deleting news: {e}")
            return None
    
    def close(self):
        """
        关闭数据库连接
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    try:
        db_manager = SQLiteDBManager()
        logger.info("Database manager initialized successfully")
        
        # 测试查询
        news_list = db_manager.get_all_news(limit=10)
        logger.info(f"Got {len(news_list)} news items")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
