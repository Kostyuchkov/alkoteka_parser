# Alkoteka Parser (Scrapy)

Парсер товаров **alkoteka.com** через публичное API `/web-api/v1/product`
для региона **Краснодар**.  
Собирает ≥ 100 товаров из каждой указанной категории и сохраняет в `result.json`
полностью по требуемому шаблону.

## Запуск

```bash
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
scrapy crawl alkoteka_api -O result.json
