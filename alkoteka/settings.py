from pathlib import Path
from fake_useragent import UserAgent
from dotenv import load_dotenv

BOT_NAME = "alkoteka"

SPIDER_MODULES = ["alkoteka.spiders"]
NEWSPIDER_MODULE = "alkoteka.spiders"

# ► случайный, но «фиксированный» User-Agent (fail-safe, без лишних warning)
USER_AGENT = UserAgent(os="windows").random
FAKE_USERAGENT_RANDOM_FAILSAFE = True

ROBOTSTXT_OBEY = False
LOG_LEVEL = "INFO"

# ► вывод
FEEDS = {
    "result.json": {
        "format": "json",
        "encoding": "utf-8",
        "ensure_ascii": False,
        "indent": 2,
    }
}

# ► сеть
DOWNLOAD_DELAY = 1.0
CONCURRENT_REQUESTS = 8
RETRY_TIMES = 3
DEPTH_LIMIT = 30
HTTPERROR_ALLOWED_CODES = [301, 302]

# ► middleware
DOWNLOADER_MIDDLEWARES = {
    "alkoteka.middlewares.KrasnodarMiddleware": 543,
    "alkoteka.middlewares.ProxyMiddleware": 544,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}

# ► читаем .env (если нужен приватный список прокси)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# запреты на «чужие» домены мешают после 301-редиректа
OFFSITE_ENABLED = False
