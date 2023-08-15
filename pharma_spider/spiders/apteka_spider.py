import time
import scrapy
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapy import signals
from pydispatch import dispatcher

options = Options()
options.add_experimental_option(
    'prefs',
    {
        'profile.managed_default_content_settings.javascript': 1,
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.mixed_script': 1,
        'profile.managed_default_content_settings.media_stream': 2,
        'profile.managed_default_content_settings.stylesheets': 2
    }
)

''' Additional functions '''


def count_items(value):
    nums = re.findall(r"\d+", value)
    return nums[0]


def get_rpc_from_url(url):
    return int(str(url).split(sep="_")[-1])


def quantity_pharmacies_with_product(text_with_number):
    quantity = re.search(r'\d+', text_with_number).group()
    return quantity


def get_float_price_from_string(string):
    return string.split(sep=" ")[1]


def click_tomsk_city(webdriver_cities):
    for city in webdriver_cities:
        if "Томск" in city.text:
            return city.click()
        else:
            pass


class PharmaSpider(scrapy.Spider):
    name = "apteka"
    allowed_domains = ['apteka-ot-sklada.ru']
    start_urls = [
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-sustavov/balzamy_-krema-dlya-sustavov',
        'https://apteka-ot-sklada.ru/catalog/izdeliya-meditsinskogo-naznacheniya/dlya-inektsiy/igly-dlya-inektsiy',
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-serdechno_sosudistoy-sistemy/serdechnoe'
        '-vnutr']

    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(7)
        self.driver.get("https://apteka-ot-sklada.ru/")
        city_selection_window = self.driver.find_element\
            (By.CSS_SELECTOR, "a[class='ui-link layout-city-confirm-dialog__reset ui-link_theme_secondary']")
        city_selection_window.click()
        region_tomskaya = self.driver.find_element(By.XPATH, '//*[contains(text(), "Томская")]')
        region_tomskaya.click()
        time.sleep(2)
        click_tomsk_city(self.driver.find_elements(By.XPATH, "//span[@class='ui-link__text']/ancestor::a[1]"))
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()
        self.driver.quit()

    def parse(self, response):
        try:
            self.driver.get(response.url)
        except TimeoutException:
            self.driver.refresh()
            
        number_products_in_category = self.driver.find_element(By.CSS_SELECTOR,
                                                               "div[class='page-header__description']").text
        counter = int(count_items(
            number_products_in_category)) // 12  # How many times 12 in the total number of products in the category
        for i in range(0, counter + 1):
            if i == 0:
                next_page = f'{response.url}?start={0}'
            else:
                next_page = f'{response.url}?start={i * 12}'
            yield scrapy.Request(url=next_page, callback=self.parse_category_pages)

    def parse_category_pages(self, response):
        try:
            self.driver.get(response.url)
        except TimeoutException:
            self.driver.refresh()

        product_links = self.driver.find_elements(By.XPATH,
                                                  '//div[@class="goods-card__name text text_size_default '
                                                  'text_weight_medium"]/a')
        link_urls = [link.get_attribute("href") for link in product_links]

        for link in link_urls:
            yield scrapy.Request(url=link, callback=self.parse_product_page)

    def parse_product_page(self, response):
        try:
            self.driver.get(response.url)
        except TimeoutException:
            self.driver.refresh()

        ''' URL section '''
        url = response.url
        ''' Title section '''
        title = self.driver.find_element(By.XPATH, '//header/h1[@class="text text_size_display-1'
                                                   ' text_weight_bold"]/span').text
        ''' RPC section '''
        rpc = get_rpc_from_url(str(url))
        ''' Marketing tags section '''
        marketing_tags = ""
        find_marketing_tags = self.driver.find_elements(By.CSS_SELECTOR, 'span[class="ui-tag'
                                                                         ' text text_weight_medium'
                                                                         ' ui-tag_theme_secondary"]')
        marketing_tags_list = []
        if find_marketing_tags:
            for elem in find_marketing_tags:
                marketing_tags_list.append(elem.text)
            marketing_tags = marketing_tags_list
        ''' Brand  section'''
        brand = self.driver.find_element(By.XPATH, '//span[@itemtype="legalName"]').text
        ''' Section section '''
        section = self.driver.find_elements(By.XPATH, '//div[@class="ui-breadcrumbs text'
                                                      ' text_weight_medium page-header__breadcrumbs'
                                                      ' text text_size_caption"]'
                                                      '/ul/li/a/span/span')

        section_hierarchy_list = []
        for element in section:
            if element.text != "Главная" and element.text != "Каталог":
                section_hierarchy_list.append(element.text)
        ''' Price section'''
        try:
            price_string = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/"
                                                              "main/section[1]/div/aside/"
                                                              "div/div[1]/ul/li/a/span/span").text
            price_value = float(get_float_price_from_string(price_string))
            price = {"original": price_value
                     }

        except NoSuchElementException:
            price = {"original": "No data"
                     }
        ''' In stock and count pharmacies section '''
        try:
            pharmacies = self.driver.find_element(By.XPATH, "/html/body/div[1]/"
                                                            "div/div/div[3]/main/section[1]/"
                                                            "div/aside/div/div[1]/ul/li/a/span").text
            pharmacies_with_product = int(quantity_pharmacies_with_product(pharmacies))
            stock = {"in_stock": True,
                     "count_pharmacies": pharmacies_with_product,
                     }
        except NoSuchElementException:
            stock = {"in_stock": False,
                     "count_pharmacies": 0,
                     }

        ''' Images section '''
        images = self.driver.find_elements(By.XPATH,
                                           "//img[@class='ui-gallery-modal__picture"
                                           " ui-gallery-modal__picture_preview']")
        big_images_list = []
        main_img = images[0].get_attribute("src")
        image_dict = {
            "main_image": main_img,
            "set_images": big_images_list,
        }
        for image in images:
            img_src = image.get_attribute("src")
            big_images_list.append(img_src)
        ''' Description section '''
        try:
            description_text = self.driver.find_element(By.XPATH, "//div[@class='custom-html content-text']").text
        except NoSuchElementException:
            description_text = "No description"

        country = self.driver.find_element(By.XPATH, "//span[@itemtype='location']").text
        metadata = {
            "description": description_text,
            "СТРАНА ПРОИЗВОДИТЕЛЬ": country

        }

        yield {
            "timestamp": int(time.time()),
            "rpc": rpc,
            "url": url,
            "title": title,
            "marketing_tags": marketing_tags,
            "brand": brand,
            "section": section_hierarchy_list,
            "price_data": price,
            "stock": stock,
            "assets": image_dict,
            "metadata": metadata,

        }
