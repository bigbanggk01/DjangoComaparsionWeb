from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import mysql.connector
    


class SendoCrawler():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testscrape"
    )
    
    mycursor = mydb.cursor()

    def __init__(self):
        pass
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def get_cat(self):
        s = Service('geckodriver.exe')
        cap = DesiredCapabilities().FIREFOX
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=s, capabilities=cap ,options=options)

        driver.get('https://www.sendo.vn/sitemap')
        driver.maximize_window()
        driver.implicitly_wait(20)
        tmp_cate_links = driver.find_elements(By.CLASS_NAME,"cat_2URx")
        item = {}
        for link in tmp_cate_links:
            #cate_links.append(link.get_attribute('href'))
            item = {
                'url':link.get_attribute('href'),
                'category':link.get_attribute('text')
            }
            sql = "INSERT INTO cate_sendo (url, category) VALUES (%s, %s)"
            val = (item['url'], item['category'])
            print(item)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        driver.close()
        
    def get_product(self):
        
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="testscrape"
            )
            mycursor = mydb.cursor(dictionary=True)
            cate_links_sql = "SELECT url,category FROM cate_sendo"
            mycursor.execute(cate_links_sql)
            cate_links = mycursor.fetchall()
        except Exception as e:
            print(e)
        s = Service('geckodriver.exe')
        cap = DesiredCapabilities().FIREFOX
        options = webdriver.FirefoxOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-browser-side-navigation')
        driver = webdriver.Firefox(service=s, capabilities=cap ,options=options)
        for link in cate_links:
            driver.get(link['url'])
            driver.maximize_window()
            driver.implicitly_wait(1.5)
            tmp_link = link['url'] + "?page="
            driver.delete_all_cookies()
            page = 1
            while page < 166:
                for i in range(13):
                        driver.execute_script("window.scrollBy(0, 400)")
                        sleep(0.1)
                        try:
                            source_element = driver.find_element(By.XPATH,'//button[@class="closeBtn_2C0k"]')
                            driver.implicitly_wait(1)
                            action = ActionChains(driver)
                            action.move_to_element(source_element)
                            action.click(source_element)
                            action.perform()
                        except:
                            continue        
                try:
                    elements = driver.find_elements(By.XPATH,'//a[@aria-label="item_3x07"]')
                    for i in elements :
                        item ={
                            'name'       : i.find_element(By.XPATH,'.//h3[@class="productName_u171"]/span').text,
                            'price'      : i.find_element(By.XPATH,'.//strong[@class="currentPrice_2hr9"]').text.replace('đ','').replace('.',''),
                            'category'   : link['category'],
                            'url'        : i.get_attribute('href'),
                            'image_link' : i.find_element(By.XPATH,'.//div[@class="thumbnail_3tZG"]/figure/img').get_attribute('src'),
                        }
                        sql = "INSERT INTO product_sendo (url, name, price, image_link, category) VALUES (%s, %s, %s, %s, %s)"
                        val = (item['url'], item['name'], item['price'], item['image_link'], item['category'] )
                        print(item)
                        mycursor.execute(sql, val)
                        mydb.commit()
                    page = page + 1 
                    new_url = tmp_link.split('?')[0]+'?page='+str(page)
                    print('[INFO] Next page: ' + new_url)
                    driver.set_page_load_timeout(20)
                    driver.implicitly_wait(2)
                    driver.get(new_url)
                except Exception as e:
                    print(e)
                    break


crawler = SendoCrawler()
crawler.get_product()