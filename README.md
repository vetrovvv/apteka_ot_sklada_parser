# apteka_ot_sklada_parser

This repository contains a Scrapy spider for scraping data from the website "https://apteka-ot-sklada.ru/".
in apteka_spider.py we have 
start_urls = [
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-sustavov/balzamy_-krema-dlya-sustavov',
        'https://apteka-ot-sklada.ru/catalog/izdeliya-meditsinskogo-naznacheniya/dlya-inektsiy/igly-dlya-inektsiy',
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-serdechno_sosudistoy-sistemy/serdechnoe'
        '-vnutr']
        # we can add to this list any categories urls in this site
## Installation

1. **Clone the repository:**
1) git clone https://github.com/vetrovvv/apteka_ot_sklada_parser.git
2) create any python project and activate venv with python 3.10 interpreter
3) add cloned repository to project directory
4) cd apteka_ot_sklada_parser
5) pip install -r requirements.txt
6) cd /apteka_ot_sklada_parser/pharma_spider/spiders
7) scrapy runspider apteka_spider.py

### Other info
You can add any proxies in settings to ROTATING_PROXY_LIST

