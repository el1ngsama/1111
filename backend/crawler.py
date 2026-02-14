import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import time
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DetikCrawler:
    def __init__(self):
        self.base_url = "https://www.detik.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.last_crawled_index = 0
        self.crawled_urls = set()
        self.retry_count = 0
        self.max_retries = 3
        self.retry_delay = 5

    def get_news_list(self, date):
        """
        获取指定日期的新闻列表
        :param date: 日期字符串，格式为 YYYY-MM-DD
        :return: 新闻列表，每个元素包含标题、URL、发布时间、封面图URL
        """
        try:
            # 尝试使用指定的日期URL
            url = f"{self.base_url}/news/indeks/{date.replace('-', '/')}"
            logger.info(f"Crawling news from: {url}")
            
            # 增加超时时间到60秒
            response = requests.get(url, headers=self.headers, timeout=60)
            
            # 如果指定日期的URL返回404，则使用主页获取最新新闻
            if response.status_code == 404:
                logger.warning(f"Date {date} not found, falling back to main page")
                url = f"{self.base_url}/"
                logger.info(f"Crawling news from: {url}")
                response = requests.get(url, headers=self.headers, timeout=60)
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 查找新闻卡片 - 尝试多种选择器
            news_cards = soup.find_all('article', class_='list-content__item')
            if not news_cards:
                news_cards = soup.find_all('div', class_='list-content__item')
            if not news_cards:
                news_cards = soup.find_all('article')
            
            logger.info(f"Found {len(news_cards)} news items")
            
            for card in news_cards:
                try:
                    # 标题和链接 - 尝试多种选择器
                    title_elem = card.find('h3', class_='media__title')
                    if not title_elem:
                        title_elem = card.find('h3')
                    if not title_elem:
                        title_elem = card.find('h2')
                    
                    if not title_elem:
                        logger.warning("No title element found, skipping card")
                        continue
                    
                    title = title_elem.text.strip()
                    
                    link_elem = title_elem.find('a')
                    if not link_elem:
                        link_elem = card.find('a')
                    
                    if not link_elem:
                        logger.warning("No link element found, skipping card")
                        continue
                    
                    news_url = link_elem.get('href')
                    if not news_url:
                        logger.warning("No URL found, skipping card")
                        continue
                    
                    if not news_url.startswith('http'):
                        news_url = self.base_url + news_url
                    
                    # 数据去重检查
                    if news_url in self.crawled_urls:
                        logger.info(f"Skipping duplicate URL: {news_url}")
                        continue
                    
                    self.crawled_urls.add(news_url)
                    
                    # 发布时间
                    time_elem = card.find('span', class_='media__date')
                    if not time_elem:
                        time_elem = card.find('span', class_='date')
                    
                    if not time_elem:
                        published_at = datetime.now().isoformat()
                    else:
                        published_at = time_elem.text.strip()
                    
                    # 封面图
                    image_elem = card.find('img', class_='media__image')
                    if not image_elem:
                        image_elem = card.find('img')
                    
                    image_url = image_elem.get('src') if image_elem else None
                    
                    news_items.append({
                        'title': title,
                        'url': news_url,
                        'published_at': published_at,
                        'image_url': image_url
                    })
                    
                    # 更新断点续爬位置
                    self.last_crawled_index += 1
                    
                    # 每爬取50条新闻，保存一次断点
                    if self.last_crawled_index % 50 == 0:
                        self.save_checkpoint(date, self.last_crawled_index)
                        
                except Exception as e:
                    logger.error(f"Error parsing news card: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(news_items)} news items")
            return news_items
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout crawling news list (60s limit reached)")
            return self._retry_with_backoff(date)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error crawling news list: {e}")
            return self._retry_with_backoff(date)
        except Exception as e:
            logger.error(f"Error crawling news list: {e}")
            return []
    
    def _retry_with_backoff(self, date):
        """
        使用指数退避策略重试
        """
        if self.retry_count >= self.max_retries:
            logger.error(f"Max retries ({self.max_retries}) reached, giving up")
            return []
        
        self.retry_count += 1
        delay = self.retry_delay * (2 ** (self.retry_count - 1))
        logger.info(f"Retrying in {delay} seconds... (attempt {self.retry_count}/{self.max_retries})")
        time.sleep(delay)
        return self.get_news_list(date)
    
    def save_checkpoint(self, date, index):
        """
        保存断点续爬位置
        """
        checkpoint_file = 'crawler_checkpoint.json'
        try:
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'date': date,
                    'last_index': index,
                    'timestamp': datetime.now().isoformat()
                }, f)
            logger.info(f"Checkpoint saved: {date}, index: {index}")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
    
    def load_checkpoint(self, date):
        """
        加载断点续爬位置
        """
        checkpoint_file = 'crawler_checkpoint.json'
        try:
            if os.path.exists(checkpoint_file):
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                    if checkpoint.get('date') == date:
                        self.last_crawled_index = checkpoint.get('last_index', 0)
                        logger.info(f"Checkpoint loaded: {date}, index: {self.last_crawled_index}")
        except Exception as e:
            logger.error(f"Error loading checkpoint: {e}")
    
    def get_article_detail(self, url):
        """
        获取文章详情
        :param url: 文章 URL
        :return: 文章详情，包含标题、发布时间、正文内容、图片列表
        """
        try:
            logger.info(f"Crawling article detail from: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 标题
            title_elem = soup.find('h1', class_='detail__title')
            title = title_elem.text.strip() if title_elem else ''
            
            # 发布时间
            time_elem = soup.find('div', class_='detail__date')
            published_at = time_elem.text.strip() if time_elem else datetime.now().isoformat()
            
            # 正文内容
            content_elem = soup.find('div', class_='detail__body')
            paragraphs = []
            images = []
            
            if content_elem:
                # 提取段落
                p_elems = content_elem.find_all('p')
                for p in p_elems:
                    text = p.text.strip()
                    if text:
                        paragraphs.append(text)
                
                # 提取图片
                img_elems = content_elem.find_all('img')
                for img in img_elems:
                    img_url = img.get('src')
                    if img_url:
                        images.append(img_url)
            
            return {
                'title': title,
                'published_at': published_at,
                'content': '\n'.join(paragraphs),
                'paragraphs': paragraphs,
                'images': images
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout crawling article detail (30s limit reached)")
            return self._retry_article_with_backoff(url)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error crawling article detail: {e}")
            return self._retry_article_with_backoff(url)
        except Exception as e:
            logger.error(f"Error crawling article detail: {e}")
            return {
                'title': '',
                'published_at': datetime.now().isoformat(),
                'content': '',
                'paragraphs': [],
                'images': []
            }
    
    def _retry_article_with_backoff(self, url):
        """
        使用指数退避策略重试文章详情
        """
        if self.retry_count >= self.max_retries:
            logger.error(f"Max retries ({self.max_retries}) reached for article, giving up")
            return {
                'title': '',
                'published_at': datetime.now().isoformat(),
                'content': '',
                'paragraphs': [],
                'images': []
            }
        
        self.retry_count += 1
        delay = self.retry_delay * (2 ** (self.retry_count - 1))
        logger.info(f"Retrying article in {delay} seconds... (attempt {self.retry_count}/{self.max_retries})")
        time.sleep(delay)
        return self.get_article_detail(url)
    
    def crawl_yesterday_news(self):
        """
        抓取昨天的所有新闻
        :return: 昨天的新闻列表
        """
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        logger.info(f"Crawling news for yesterday: {yesterday}")
        
        # 加载断点
        self.load_checkpoint(yesterday)
        
        return self.get_news_list(yesterday)

if __name__ == "__main__":
    crawler = DetikCrawler()
    # 测试抓取昨天的新闻
    news_list = crawler.crawl_yesterday_news()
    logger.info(f"Crawled {len(news_list)} news items from yesterday")