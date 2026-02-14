-- Cloudflare D1 数据库表结构
-- 印尼新闻应用数据库初始化脚本

-- 创建 news_feed 表（新闻列表）
CREATE TABLE IF NOT EXISTS news_feed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT UNIQUE NOT NULL,
    title_cn TEXT,
    title_id TEXT NOT NULL,
    thumbnail_r2_url TEXT,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    content_structure TEXT,
    is_crawled BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建 vocabulary 表（词汇表）
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_article_id) REFERENCES news_feed(id) ON DELETE CASCADE
);

-- 创建 daily_digest 表（日报）
CREATE TABLE IF NOT EXISTS daily_digest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE NOT NULL,
    digest_items TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_news_feed_published_at ON news_feed(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_feed_is_crawled ON news_feed(is_crawled);
CREATE INDEX IF NOT EXISTS idx_news_feed_original_url ON news_feed(original_url);
CREATE INDEX IF NOT EXISTS idx_vocabulary_word_selected ON vocabulary(word_selected);
CREATE INDEX IF NOT EXISTS idx_vocabulary_is_archived ON vocabulary(is_archived);
CREATE INDEX IF NOT EXISTS idx_vocabulary_source_article_id ON vocabulary(source_article_id);
CREATE INDEX IF NOT EXISTS idx_daily_digest_date ON daily_digest(date DESC);

-- 插入测试数据（可选）
-- INSERT INTO news_feed (original_url, title_cn, title_id, published_at, is_crawled) VALUES
--     ('https://www.detik.com/test1', '测试新闻标题1', 'Test News Title 1', '2025-02-10 10:00:00', 0),
--     ('https://www.detik.com/test2', '测试新闻标题2', 'Test News Title 2', '2025-02-10 11:00:00', 0);

-- INSERT INTO vocabulary (word_selected, meaning_cn, root_word, pos, vibe_check, context_sentence_id) VALUES
--     ('kabar', '消息', 'kabar', '名词', '正式用语，常用于新闻报道', 'Ini adalah kabar terbaru hari ini.'),
--     ('berita', '新闻', 'berita', '名词', '常用词，指新闻报道', 'Berita ini sangat menarik.');
