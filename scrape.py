from bs4 import BeautifulSoup
from urllib.request import urlopen

class Scraper:

    obj_infos = {}

    
    def __init__(self, product_need, seperator_tag, separator_attr, separator_val, weburl):
        self.product_need = product_need
        self.url = weburl
        self.separator_tag = seperator_tag
        self.separator_attr = separator_attr
        self.separator_val = separator_val
        url_to_srape = self.url + self.product_need.replace(' ','+')
        self.html_doc = urlopen(url_to_srape)
        self.bsObj = BeautifulSoup(self.html_doc, 'html.parser')
        self.separator_obj = self.bsObj.find(self.separator_tag,{self.separator_attr : self.separator_val})

    def find_all_separator(self):
        tmp_obj = self.bsObj.find_all(self.separator_tag,{self.separator_attr : self.separator_val})
        return tmp_obj

    def find_obj_info(seft, codes):
        tmp_obj = seft.separator_obj
        obj_infos = []
        obj_info = {}
        
        for code in codes:
            i = 0
            while len(code) > i:
                if code[i] == '1':
                    tmp_obj = tmp_obj.find()
                elif code[i]=='0':
                    tmp_obj = tmp_obj.next_sibling
                elif code[i]=='2':
                    tmp_obj = tmp_obj
                i=i+1
            obj_info['name'] = tmp_obj.name
            obj_info['attr'] = tmp_obj.attrs
            tmp_obj = seft.separator_obj
            dictionary_copy = obj_info.copy()
            obj_info.clear()
            obj_infos.append(dictionary_copy)
        return obj_infos

    def set_product_info(self):

    
    def find_product_info(self, obj, obj_infos):
        product_infos = []
        product_info = {}
        i = 0
        for obj_info in obj_infos:
            
            tmp_obj = obj.find(obj_info['name'],obj_info['attr'])
            
            if i == 0:
                product_info['name'] = tmp_obj.get_text()
            elif i == 1:
                product_info['price'] = tmp_obj.get_text()
            else:
                if obj.name == 'a':
                    product_info['url'] = obj['href']
                else: 
                    product_info['url'] = obj.find('a', href = True)['href']                    
            i=i+1
            dictionary_copy = product_info.copy()
            product_info.clear()
            product_infos.append(dictionary_copy)
        return product_infos


scraper = Scraper('laptop asus', 'a', 'class', 'product-item', 'https://tiki.vn/search?q=')
objs = scraper.find_all_separator()
for obj in objs:
    print(scraper.find_product_info(obj, scraper.find_obj_info(['1110010','1110010001','2'])))