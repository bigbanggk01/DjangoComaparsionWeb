from time import sleep
from scrapy import item
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
s = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=s,options=options)
driver.get('https://www.sendo.vn/sitemap')
driver.maximize_window()
driver.implicitly_wait(20)

tmp_cate_links = driver.find_elements(By.CLASS_NAME,"cat_2URx")
cate_links = []
for link in tmp_cate_links:
    cate_links.append(link.get_attribute('href'))

bunch_of_links = []
tmp_cate_links_2 = []
for link in cate_links:
    link = link + '?page='
    tmp_cate_links_2.append(link)

# for link in tmp_cate_links_2:
#     for i in range(0,100):
#         link_tmp = ''
#         link_tmp = link + str(i)
#         bunch_of_links.append(link_tmp)
        
# print(bunch_of_links)
item = {}
items = []
def run():
    for link in tmp_cate_links_2:
        for i in range(0,200):
            driver.get(link+str(i))
            driver.implicitly_wait(1)
            for i in range(10):
                driver.execute_script("window.scrollBy(0,600)")
                sleep(0.2)
                try:
                    source_element = driver.find_element(By.XPATH,'//button[@class="closeBtn_2C0k"]')
                    action = ActionChains(driver)
                    action.move_to_element(source_element)
                    sleep(0.1)
                    action.click()
                    action.perform()
                except:
                    pass
                    
            try:
                elements = driver.find_elements(By.XPATH,'//a[@aria-label="item_3x07"]')
                for i in elements:
                    item['name'] = i.find_element(By.XPATH,'.//h3[@class="productName_u171"]/span').text
                    item['price'] = i.find_element(By.XPATH,'.//strong[@class="currentPrice_2hr9"]').text
                    item['url'] = i.get_attribute('href')
                    item['image_link']= i.find_element(By.XPATH,'.//div[@class="thumbnail_3tZG"]/figure/img').get_attribute('src')
                    print(item)

            except:
                break
run()
driver.quit()