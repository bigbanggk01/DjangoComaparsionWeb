import subprocess
subprocess.run(['scrapy','crawl','test',
# '-a','urls=https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567,https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567?page=1',
'-a','items_xpath=//div[@data-sqe="item"]', 
'-a','url_xpath=.//a[@data-sqe="link"]/@href',
'-a','name_xpath=.//div[@data-sqe="name"]/div[1]/div[1]/text()',
'-a','price_xpath=.//div[@class="zp9xm9"]/text()',
'-a','image_xpath=.//a[@data-sqe="link"]/div[1]/div[1]/div[1]/img/@src[1]'])