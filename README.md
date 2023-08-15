# apteka_ot_sklada_parser

This repository contains a Scrapy spider for scraping data from the website "https://apteka-ot-sklada.ru/".
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
in apteka_spider.py we have 
start_urls = [
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-sustavov/balzamy_-krema-dlya-sustavov',
        'https://apteka-ot-sklada.ru/catalog/izdeliya-meditsinskogo-naznacheniya/dlya-inektsiy/igly-dlya-inektsiy',
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-serdechno_sosudistoy-sistemy/serdechnoe'
        '-vnutr']
we can add to this list any categories urls in this site


You can add any proxies in settings to ROTATING_PROXY_LIST,in repository now is only 1 free proxie,change it for stability work

after "scrapy runspider apteka_spider.py" a result.json file will be created


Example of 1 parsed page information:

{"timestamp": 1692117914, "rpc": 866062660, "url": "https://apteka-ot-sklada.ru/catalog/V-Dikul-Forte-balzam-dlya-sustavov-125ml_866062660", "title": "В.Дикуль Форте бальзам для суставов 125мл", "marketing_tags": "", "brand": "ООО КоролевФарм", "section": ["Медикаменты и БАДы", "Заболевания суставов", "Бальзамы, крема для суставов"], "price_data": {"original": "No data"}, "stock": {"in_stock": false, "count_pharmacies": 0}, "assets": {"main_image": "https://apteka-ot-sklada.ru/images/goods/866062660.jpg", "set_images": ["https://apteka-ot-sklada.ru/images/goods/866062660.jpg"]}, "metadata": {"description": "Описание\nИмя Валентина Ивановича Дикуля сегодня известно всему миру. Выдающийся врач, создавший уникальную методику восстановления двигательных функций после спинномозговой травмы, при тяжелых суставных недугах, академик РАМН, профессор, доктор медицинских наук, мастер спорта.\nСегодня по его методике работают многие медицинские реабилитационные Центры в России и за рубежом. Тысячи людей обязаны ему возвращением к Жизни.\nПомочь в преодолении суставных недугов призван новый целебный бальзам, разработанный В. Дикулем совместно со специалистами компании Фора-Фарм.\nБальзам поможет восстановлению двигательных функций при суставных травмах (ушибах, растяжениях, переломах), предотвратит развитие радикулита, остеохондрозов, артритов и артрозов и обеспечит успех комплексного лечения при запущенных формах этих заболеваний.", "СТРАНА ПРОИЗВОДИТЕЛЬ": "Россия"},

