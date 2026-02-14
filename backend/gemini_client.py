import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        """
        初始化 Gemini 客户端
        """
        try:
            self.api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
            
            if not self.api_key:
                raise ValueError("缺少 GOOGLE_GEMINI_API_KEY 环境变量")
            
            # 配置 Gemini
            genai.configure(api_key=self.api_key)
            
            # 初始化模型
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
            logger.info("Gemini client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {e}")
            raise
    def translate(self, text, target_language='zh-CN'):
        """
        翻译文本
        :param text: 待翻译的文本
        :param target_language: 目标语言，默认为中文
        :return: 翻译后的文本
        """
        try:
            if not text:
                return text
            
            prompt = f"请将以下文本翻译成{target_language}，保持原意准确，语言自然流畅：\n\n{text}"
            
            # 设置较短的超时时间
            import google.generativeai.types as types
            generation_config = types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=256,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={"timeout": 30}  # 30秒超时
            )
            translated_text = response.text.strip()
            
            logger.info(f"Translated text: {text[:50]}... -> {translated_text[:50]}...")
            return translated_text
            
        except Exception as e:
            error_str = str(e)
            # 检查是否是配额问题
            if '429' in error_str or 'quota' in error_str.lower() or 'exceeded' in error_str.lower():
                logger.warning(f"Gemini API quota exceeded: {e}")
                # 抛出配额异常，让调用者能够处理
                raise Exception(f"Quota exceeded: {e}")
            else:
                logger.error(f"Error translating text: {e}")
                return text  # 其他错误时返回原文
    def translate_news(self, news_list):
        """
        翻译新闻列表
        :param news_list: 新闻列表
        :return: 翻译后的新闻列表
        """
        try:
            translated_news_list = []
            quota_exceeded = False
            
            for news in news_list:
                try:
                    if news.get('title'):
                        # 翻译标题
                        translated_title = self.translate(news['title'])
                        news['title_cn'] = translated_title
                    else:
                        # 如果没有标题，设置空字符串
                        news['title_cn'] = ''
                    translated_news_list.append(news)
                except Exception as e:
                    logger.error(f"Error translating news: {e}")
                    # 检查是否是配额问题
                    if '429' in str(e) or 'quota' in str(e).lower():
                        quota_exceeded = True
                    # 翻译失败时，仍然使用原标题
                    news['title_cn'] = news.get('title', '')
                    translated_news_list.append(news)
            
            # 如果配额用完，记录警告
            if quota_exceeded:
                logger.warning("Gemini API quota exceeded, using original text instead")
            
            return translated_news_list
            
        except Exception as e:
            logger.error(f"Error translating news list: {e}")
            # 整体翻译失败时，确保每个新闻都有title_cn字段
            for news in news_list:
                if 'title_cn' not in news:
                    news['title_cn'] = news.get('title', '')
            return news_list
    def translate_article(self, article_detail):
        """
        翻译文章详情
        :param article_detail: 文章详情
        :return: 翻译后的文章详情
        """
        try:
            quota_exceeded = False
            
            if article_detail.get('title'):
                # 翻译标题
                try:
                    translated_title = self.translate(article_detail['title'])
                    article_detail['title_cn'] = translated_title
                except Exception as e:
                    logger.error(f"Error translating title: {e}")
                    if '429' in str(e) or 'quota' in str(e).lower():
                        quota_exceeded = True
                    article_detail['title_cn'] = article_detail.get('title', '')
            
            if article_detail.get('paragraphs'):
                # 翻译段落
                translated_paragraphs = []
                for paragraph in article_detail['paragraphs']:
                    try:
                        translated_paragraph = self.translate(paragraph)
                        translated_paragraphs.append(translated_paragraph)
                    except Exception as e:
                        logger.error(f"Error translating paragraph: {e}")
                        if '429' in str(e) or 'quota' in str(e).lower():
                            quota_exceeded = True
                        translated_paragraphs.append(paragraph)  # 翻译失败时使用原文
                article_detail['paragraphs_cn'] = translated_paragraphs
            
            # 如果配额用完，记录警告
            if quota_exceeded:
                logger.warning("Gemini API quota exceeded during article translation, using original text instead")
            
            return article_detail
            
        except Exception as e:
            logger.error(f"Error translating article: {e}")
            return article_detail
    def analyze_word(self, word, context=None):
        """
        分析单词
        :param word: 待分析的单词
        :param context: 单词所在的上下文
        :return: 单词分析结果
        """
        try:
            if not word:
                return None
            
            prompt = f"请分析以下印尼语单词：{word}\n"
            
            if context:
                prompt += f"上下文：{context}\n"
            
            prompt += "\n请提供以下信息：\n"
            prompt += "1. 中文释义\n"
            prompt += "2. 词根\n"
            prompt += "3. 词性\n"
            prompt += "4. 用法说明（语感、使用场景等）\n"
            prompt += "5. 例句（如果有上下文请使用原句）\n"
            
            response = self.model.generate_content(prompt)
            
            # 解析响应
            analysis_result = {
                'word': word,
                'meaning_cn': '',
                'root_word': '',
                'pos': '',
                'vibe_check': '',
                'context_sentence_id': context or ''
            }
            
            response_text = response.text.strip()
            lines = response_text.split('\n')
            
            for line in lines:
                if '中文释义' in line:
                    analysis_result['meaning_cn'] = line.split('：', 1)[1].strip() if '：' in line else line.strip()
                elif '词根' in line:
                    analysis_result['root_word'] = line.split('：', 1)[1].strip() if '：' in line else line.strip()
                elif '词性' in line:
                    analysis_result['pos'] = line.split('：', 1)[1].strip() if '：' in line else line.strip()
                elif '用法说明' in line:
                    analysis_result['vibe_check'] = line.split('：', 1)[1].strip() if '：' in line else line.strip()
                elif '例句' in line:
                    analysis_result['context_sentence_id'] = line.split('：', 1)[1].strip() if '：' in line else line.strip()
            
            logger.info(f"Analyzed word: {word}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing word: {e}")
            return None
    def generate_summary(self, content):
        """
        生成摘要
        :param content: 待摘要的内容
        :return: 摘要文本
        """
        try:
            if not content:
                return ""
            
            prompt = f"请为以下内容生成简洁的中文摘要，长度控制在100字以内：\n\n{content}"
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            logger.info(f"Generated summary: {summary[:100]}...")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""

if __name__ == "__main__":
    # 测试 Gemini 客户端
    try:
        gemini = GeminiClient()
        
        # 测试翻译
        test_text = "Presiden Jokowi meninjau perkembangan pembangunan IKN"
        translated = gemini.translate(test_text)
        print(f"Original: {test_text}")
        print(f"Translated: {translated}")
        
        # 测试单词分析
        test_word = "meninjau"
        test_context = "Presiden Jokowi meninjau perkembangan pembangunan IKN"
        analysis = gemini.analyze_word(test_word, test_context)
        print(f"Word analysis: {analysis}")
        
        # 测试摘要生成
        test_content = "Presiden Jokowi meninjau perkembangan pembangunan IKN hari ini, dia merasa puas dengan pekerjaan saat ini. Ia mengatakan bahwa pembangunan infrastruktur telah mencapai 80%, diperkirakan akan selesai seluruhnya sebelum akhir 2024."
        summary = gemini.generate_summary(test_content)
        print(f"Summary: {summary}")
        
    except Exception as e:
        print(f"Test failed: {e}")