import os
import random


class ProxyMiddleware:
    """Подставляет случайный HTTP-прокси (если указан proxies.txt)."""
    def __init__(self):
        proxy_file = os.getenv("PROXY_FILE", "proxies.txt")
        self.proxies = []
        if os.path.exists(proxy_file):
            with open(proxy_file) as f:
                self.proxies = [p.strip() for p in f if p.strip()]

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if self.proxies:
            request.meta["proxy"] = random.choice(self.proxies)


class KrasnodarMiddleware:
    """
    Фиксируем регион «Краснодар». На сайте встречаются разные имена cookie —
    ставим сразу все известные.
    """
    CITY_COOKIES = {
        "BITRIX_SM_CITY": "46",
        "BITRIX_SM_CITY_ID": "46",
        "BITRIX_SM_REGION": "46",
    }

    def process_request(self, request, spider):
        for k, v in self.CITY_COOKIES.items():
            request.cookies[k] = v
        request.cookies["BITRIX_SM_18PLUS"] = "Y"      # подтверждение 18+
