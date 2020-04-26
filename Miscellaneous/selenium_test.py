#%%
from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

options = Options()
options.add_argument("no-sandbox")
#options.add_argument("headless")
options.add_argument("enable-javascript")
driver = webdriver.Chrome(options=options)
driver.get('https://twitter.com/search?q=(%23%24SPY)&src=typed_query')


#%%

store = []

for _ in range(5):
    print('='*30)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    store = [x.text for x in soup.find_all('div', {
        'class': 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})]
    print(store)
    time.sleep(0.5)

