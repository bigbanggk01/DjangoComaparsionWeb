from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
pattern = re.compile(r"a")
html = urlopen('https://lazada.vn/')
print(BeautifulSoup(html.read(),'html.parser'))
