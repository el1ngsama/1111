import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';

function App() {
  const [newsList, setNewsList] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const [showLookupButton, setShowLookupButton] = useState(false);
  const [lookupButtonPosition, setLookupButtonPosition] = useState({ top: 0, left: 0 });
  const [lookupResult, setLookupResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLookingUp, setIsLookingUp] = useState(false);
  const [vocabulary, setVocabulary] = useState([]);
  const [highlightedWords, setHighlightedWords] = useState(new Set());
  const [showVocabulary, setShowVocabulary] = useState(false);
  const [apiError, setApiError] = useState(null);
  const articleRef = useRef(null);
  const saveTimeoutRef = useRef(null);
  const abortControllerRef = useRef(null);

  // 从本地存储加载单词本
  useEffect(() => {
    try {
      const savedVocabulary = localStorage.getItem('vocabulary');
      if (savedVocabulary) {
        const parsed = JSON.parse(savedVocabulary);
        setVocabulary(Array.isArray(parsed) ? parsed : []);
      }
    } catch (error) {
      console.error('Error loading vocabulary from localStorage:', error);
      setVocabulary([]);
    }
  }, []);

  // 保存单词本到本地存储（使用防抖）
  const saveVocabulary = useCallback((newVocabulary) => {
    setVocabulary(newVocabulary);
    
    // 清除之前的定时器
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }
    
    // 使用防抖，避免频繁写入
    saveTimeoutRef.current = setTimeout(() => {
      try {
        localStorage.setItem('vocabulary', JSON.stringify(newVocabulary));
      } catch (error) {
        console.error('Error saving vocabulary to localStorage:', error);
      }
    }, 300);
  }, []);

  // 清理定时器
  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
      // 清理AbortController
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  // 从后端 API 获取实时新闻数据
  useEffect(() => {
    const fetchNews = async () => {
      setIsLoading(true);
      setApiError(null);
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 增加到60秒超时
        
        const response = await fetch('/api/news', {
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.success) {
          setNewsList(data.data || []);
        } else {
          console.error('API returned error:', data.message);
          setApiError(data.message || '获取新闻失败');
        }
      } catch (error) {
        if (error.name === 'AbortError') {
          console.error('Request timeout: 后端API响应超时，请稍后重试');
          setApiError('请求超时，请检查网络连接或稍后重试');
        } else {
          console.error('Error fetching news:', error);
          setApiError(`获取新闻失败: ${error.message}`);
        }
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchNews();
  }, []);

  // 使用useCallback稳定getArticleDetail函数引用
  const getArticleDetail = useCallback(async (news) => {
    try {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      
      const controller = new AbortController();
      abortControllerRef.current = controller;
      const timeoutId = setTimeout(() => controller.abort(), 60000);
      
      const response = await fetch(`/api/article?url=${encodeURIComponent(news.url)}`, {
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success && data.data) {
        const content_structure = [];
        
        // 处理段落数据
        if (data.data.paragraphs && Array.isArray(data.data.paragraphs) && data.data.paragraphs.length > 0) {
          for (let i = 0; i < data.data.paragraphs.length; i++) {
            const idText = data.data.paragraphs[i] || '';
            const cnText = data.data.paragraphs_cn && data.data.paragraphs_cn[i] ? data.data.paragraphs_cn[i] : idText;
            
            if (idText.trim()) {
              content_structure.push({
                type: 'text',
                cn: cnText,
                id: idText
              });
            }
          }
        }
        
        // 处理图片数据
        if (data.data.images && Array.isArray(data.data.images)) {
          data.data.images.forEach(image_url => {
            if (image_url) {
              content_structure.push({
                type: 'image',
                url: image_url
              });
            }
          });
        }
        
        // 如果没有内容，显示提示
        if (content_structure.length === 0) {
          content_structure.push({
            type: 'text',
            cn: '暂无文章内容',
            id: 'No content available'
          });
        }
        
        return {
          ...news,
          content_structure
        };
      } else {
        console.error('API returned error or no data:', data.message);
        throw new Error(data.message || '获取文章详情失败');
      }
    } catch (error) {
      // 如果是AbortError，说明请求被取消，不应该记录为错误
      if (error.name === 'AbortError') {
        console.log('请求被取消:', error.message);
        // 返回null表示请求被取消，不显示错误信息
        return null;
      }
      
      console.error('Error fetching article detail:', error);
      // 返回错误提示而不是硬编码内容
      return {
        ...news,
        content_structure: [
          {
            type: 'text',
            cn: `无法加载文章内容: ${error.message}`,
            id: 'Error loading content'
          }
        ]
      };
    }
  }, []);

  // 处理新闻点击
  const handleNewsClick = async (news) => {
    setIsLoading(true);
    setApiError(null);
    try {
      const articleDetail = await getArticleDetail(news);
      
      if (articleDetail === null) {
        setIsLoading(false);
        return;
      }
      
      setSelectedArticle(articleDetail);
      setHighlightedWords(new Set());
      setLookupResult(null);
    } catch (error) {
      console.error('Error getting article detail:', error);
      setApiError(`加载文章失败: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // 处理返回新闻列表
  const handleBackToList = () => {
    setSelectedArticle(null);
    setLookupResult(null);
    setHighlightedWords(new Set());
    setApiError(null);
  };

  // 处理文本选择
  const handleTextSelect = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().length > 0) {
      const selectedText = selection.toString();
      setSelectedText(selectedText);
      setShowLookupButton(true);
      
      // 获取选中区域的位置
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
      
      setLookupButtonPosition({
        top: rect.bottom + scrollTop + 10,
        left: rect.left + scrollLeft
      });
    } else {
      setShowLookupButton(false);
      setLookupResult(null);
    }
  };

  // 处理单词查询
  const handleLookup = async () => {
    if (selectedText) {
      setIsLookingUp(true);
      setShowLookupButton(false);
      
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10秒超时
        
        const response = await fetch('/api/analyze/word', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: controller.signal,
          body: JSON.stringify({
            word: selectedText,
            context: selectedArticle?.content_structure?.find(item => 
              item.type === 'text' && item.id.includes(selectedText)
            )?.id || '',
            source_article_id: selectedArticle?.id
          }),
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        let result;
        
        if (data.success && data.data) {
          result = data.data;
        } else {
          // 使用模拟数据
          result = {
            word: selectedText,
            meaning_cn: '示例翻译：这是一个示例单词的中文释义',
            root_word: '示例词根',
            pos: '名词',
            vibe_check: '正式用语，常用于新闻报道',
            context_sentence_id: '这是包含该单词的完整原句示例'
          };
        }
        
        setLookupResult(result);
        
        // 标红加粗选中的单词
        setHighlightedWords(prev => new Set([...prev, selectedText]));
        
        // 保存到单词本
        const vocabularyItem = {
          id: Date.now(),
          word: selectedText,
          meaning_cn: result.meaning_cn,
          context_sentence_id: result.context_sentence_id,
          article_title: selectedArticle?.title,
          timestamp: new Date().toISOString()
        };
        
        saveVocabulary([...vocabulary, vocabularyItem]);
        
      } catch (error) {
        console.error('Error looking up word:', error);
        const mockResult = {
          word: selectedText,
          meaning_cn: '示例翻译：这是一个示例单词的中文释义',
          root_word: '示例词根',
          pos: '名词',
          vibe_check: '正式用语，常用于新闻报道',
          context_sentence_id: '这是包含该单词的完整原句示例'
        };
        setLookupResult(mockResult);
        
        // 标红加粗选中的单词
        setHighlightedWords(prev => new Set([...prev, selectedText]));
        
        // 保存到单词本
        const vocabularyItem = {
          id: Date.now(),
          word: selectedText,
          meaning_cn: mockResult.meaning_cn,
          context_sentence_id: mockResult.context_sentence_id,
          article_title: selectedArticle?.title,
          timestamp: new Date().toISOString()
        };
        
        saveVocabulary([...vocabulary, vocabularyItem]);
      } finally {
        setIsLookingUp(false);
      }
    }
  };

  // 高亮文本中的单词（使用useMemo优化性能）
  const highlightText = useCallback((text) => {
    if (!text || highlightedWords.size === 0) {
      return text;
    }
    
    let highlightedText = text;
    highlightedWords.forEach(word => {
      if (!word) return;
      
      try {
        const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escapedWord})`, 'gi');
        highlightedText = highlightedText.replace(regex, '<span class="highlighted-word">$1</span>');
      } catch (error) {
        console.error('Error highlighting word:', word, error);
      }
    });
    return highlightedText;
  }, [highlightedWords]);

  // 删除单词本中的单词
  const deleteVocabularyItem = useCallback((id) => {
    const newVocabulary = vocabulary.filter(item => item.id !== id);
    saveVocabulary(newVocabulary);
  }, [vocabulary, saveVocabulary]);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white">
      {/* 顶部导航栏 */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-primary">印尼新闻聚合</h1>
          <div className="flex gap-2">
            {selectedArticle && (
              <button
                onClick={handleBackToList}
                className="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-all"
              >
                返回列表
              </button>
            )}
            <button
              onClick={() => setShowVocabulary(!showVocabulary)}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-all"
            >
              单词本 ({vocabulary.length})
            </button>
          </div>
        </div>
      </header>

      {/* 主内容区域 */}
      <main className="container mx-auto px-4 py-6">
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
          </div>
        ) : apiError ? (
          <div className="bg-red-100 dark:bg-red-900 border-2 border-red-400 dark:border-red-600 rounded-lg p-6 text-center">
            <p className="text-red-800 dark:text-red-300 font-bold text-lg mb-2">错误</p>
            <p className="text-red-700 dark:text-red-400">{apiError}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition-all"
            >
              重新加载
            </button>
          </div>
        ) : selectedArticle ? (
          /* 文章详情页 */
          <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="news-title-cn">{selectedArticle.title_cn || selectedArticle.title || '文章标题'}</h2>
            <p className="news-title-id">{selectedArticle.title || ''}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              发布时间: {new Date(selectedArticle.published_at).toLocaleString()}
            </p>
            
            <div className="mt-6" onMouseUp={handleTextSelect} onTouchEnd={handleTextSelect} ref={articleRef}>
              {selectedArticle.content_structure.map((item, index) => (
                <div key={`${item.type}-${index}`}>
                  {item.type === 'text' && (
                    <>
                      <p className="article-paragraph-cn">[CN] {item.cn}</p>
                      <p 
                        className="article-paragraph-id"
                        dangerouslySetInnerHTML={{ __html: `[ID] ${highlightText(item.id)}` }}
                      />
                    </>
                  )}
                  {item.type === 'image' && (
                    <div className="my-6">
                      <img 
                        src={item.url} 
                        alt="新闻图片" 
                        className="w-full h-auto rounded-lg shadow-sm"
                        loading="lazy"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          console.error('Image failed to load:', item.url);
                        }}
                      />
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* 单词查询按钮 - 悬浮在选中区域附近 */}
            {showLookupButton && (
              <div 
                className="fixed z-50"
                style={{ 
                  top: `${lookupButtonPosition.top}px`, 
                  left: `${lookupButtonPosition.left}px` 
                }}
              >
                <button
                  className="lookup-button"
                  onClick={handleLookup}
                  disabled={isLookingUp}
                >
                  {isLookingUp ? '查询中...' : '查询'}
                </button>
              </div>
            )}

            {/* 查询结果 */}
            {isLookingUp ? (
              <div className="mt-8 p-4 bg-blue-50 dark:bg-gray-700 rounded-lg border-2 border-blue-300 dark:border-blue-600">
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-600 mr-3"></div>
                  <p className="text-blue-800 dark:text-blue-300">正在分析单词...</p>
                </div>
              </div>
            ) : lookupResult && (
              <div className="mt-8 p-4 bg-blue-50 dark:bg-gray-700 rounded-lg border-2 border-blue-300 dark:border-blue-600">
                <h3 className="font-bold text-lg mb-2 text-blue-800 dark:text-blue-300">单词分析</h3>
                <p><strong>单词:</strong> {lookupResult.word}</p>
                <p><strong>中文释义:</strong> {lookupResult.meaning_cn}</p>
                <p><strong>词根:</strong> {lookupResult.root_word}</p>
                <p><strong>词性:</strong> {lookupResult.pos}</p>
                <p><strong>用法说明:</strong> {lookupResult.vibe_check}</p>
                <p><strong>原句上下文:</strong> {lookupResult.context_sentence_id}</p>
                <p className="text-sm text-green-600 dark:text-green-400 mt-2">
                  ✓ 已保存到单词本
                </p>
              </div>
            )}
          </div>
        ) : (
          /* 新闻列表页 */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {newsList.map((news, index) => (
              <div 
                key={`${news.url}-${index}`} 
                className="news-card"
                onClick={() => handleNewsClick(news)}
              >
                {news.image_url && (
                  <img 
                    src={news.image_url} 
                    alt={news.title} 
                    className="w-full h-48 object-cover rounded-t-lg"
                    loading="lazy"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                <div className="p-4">
                  <h3 className="font-bold text-lg mb-2">{news.title_cn || news.title}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{news.title}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                    {new Date(news.published_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* 单词本侧边栏 */}
      {showVocabulary && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
          <div className="bg-white dark:bg-gray-800 w-full max-w-md h-full overflow-y-auto p-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">单词本</h2>
              <button
                onClick={() => setShowVocabulary(false)}
                className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                ✕
              </button>
            </div>
            
            {vocabulary.length === 0 ? (
              <p className="text-gray-500 dark:text-gray-400 text-center py-8">
                单词本为空，请在文章中选中单词进行查询
              </p>
            ) : (
              <div className="space-y-4">
                {vocabulary.map(item => (
                  <div key={item.id} className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="font-bold text-lg text-blue-600 dark:text-blue-400">{item.word}</p>
                        <p className="text-sm mt-1">{item.meaning_cn}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                          {item.context_sentence_id}
                        </p>
                        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                          {new Date(item.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <button
                        onClick={() => deleteVocabularyItem(item.id)}
                        className="text-red-500 hover:text-red-700 ml-2"
                      >
                        删除
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
