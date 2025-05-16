import json
import time
import scrapy
from alkoteka.items import AlkotekaItem


class AlkotekaApiSpider(scrapy.Spider):
    """Парсит каталог через API /web-api/v1/product"""
    name = "alkoteka_api"
    allowed_domains = ["alkoteka.com"]

    CITY_UUID = "4a70f9e0-46ae-11e7-83ff-00155d026416"   # Краснодар
    PER_PAGE = 120                                       # максимум, что даёт API

    # slug ➜ «человекочитаемый» URL (для поля section)
    CATEGORIES = {
        "slaboalkogolnye-napitki-2": "https://alkoteka.com/catalog/slaboalkogolnye-napitki-2",
        "vino":                      "https://alkoteka.com/catalog/vino",
        "krepkiy-alkogol":           "https://alkoteka.com/catalog/krepkiy-alkogol",
    }

    # ──────────────────────────────────────────────────────────────
    def start_requests(self):
        for slug in self.CATEGORIES:
            api = (
                "https://alkoteka.com/web-api/v1/product"
                f"?city_uuid={self.CITY_UUID}"
                f"&page=1&per_page={self.PER_PAGE}"
                f"&root_category_slug={slug}"
            )
            yield scrapy.Request(api, callback=self.parse_page, meta={
                "slug": slug,
                "page": 1,
            })

    # ──────────────────────────────────────────────────────────────
    def parse_page(self, response: scrapy.http.Response):
        data = json.loads(response.text)

        # 1) товары
        items = data.get("results", [])
        if not items and response.meta["page"] == 1:
            self.logger.warning("Пустая категория %s", response.meta["slug"])

        for pr in items:
            yield self.item_from_json(pr, response.meta["slug"])

        # 2) пагинация
        if data.get("meta", {}).get("has_more_pages"):
            next_page = response.meta["page"] + 1
            next_url = response.url.replace(
                f"&page={response.meta['page']}",
                f"&page={next_page}"
            )
            yield response.follow(
                next_url,
                callback=self.parse_page,
                meta={**response.meta, "page": next_page}
            )

    # ──────────────────────────────────────────────────────────────
    def item_from_json(self, pr: dict, slug: str) -> AlkotekaItem:
        """Конвертируем JSON объекта товара в AlkotekaItem."""
        img = pr.get("image_url") or ""
        price_now = pr.get("price") or 0.0
        price_old = pr.get("prev_price") or price_now
        sale_tag = f"Скидка {round((1 - price_now / price_old)*100)}%" \
                   if price_old and price_now < price_old else ""

        return AlkotekaItem(
            timestamp=int(time.time()),
            RPC=str(pr.get("vendor_code", "")),
            url=pr.get("product_url", ""),
            title=pr.get("name", ""),
            marketing_tags=[lbl.get("title", "") for lbl in pr.get("action_labels", [])],
            brand=pr.get("brand", ""),
            section=[self.CATEGORIES[slug].split("/")[-1]],
            price_data={
                "current": price_now,
                "original": price_old,
                "sale_tag": sale_tag,
            },
            stock={
                "in_stock": pr.get("available", False),
                "count": pr.get("quantity_total", 0),
            },
            assets={
                "main_image": img,
                "set_images": [img] if img else [],
                "view360": [],
                "video": [],
            },
            metadata={
                "__description": pr.get("subname", ""),
            },
            variants=0,
        )
