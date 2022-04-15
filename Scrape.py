# -*- coding: utf-8 -*-
"""

@author: Soo Kar Lok
"""

link = 'https://quotes.toscrape.com/'

def parse(r):
    from bs4 import BeautifulSoup

    if r.status_code==200:
        print('Success')
        return BeautifulSoup(r.content,'lxml')
    else:
        print('Error: '+str(r.status_code))


def preview(soup,name):
    with open(str(name)+".html", "w", encoding='utf-8') as file:
        file.write(str(soup))

def simple_scrape(link):
    import requests
    r=requests.get(link)
    return parse(r)
    
def simple_scrape_header(link,headers):
    import requests
    r=requests.get(link,headers=headers)
    return parse(r)

def cloudscraper_scrape(link):
    import cloudscraper
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False})
    r=scraper.get(link)
    return parse(r)

def selenium_scrape(link):
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    from bs4 import BeautifulSoup
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)
    print('Waiting for 30s...')
    time.sleep(30)
    r = driver.page_source
    driver.close()
    return BeautifulSoup(r, 'lxml') 

def proxies_ua_scrape(link,country_id):
    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, HardwareType
    from fp.fp import FreeProxy
    import requests
    software_names = [SoftwareName.CHROME.value]
    hardware_type = [HardwareType.MOBILE__PHONE]
    user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
    proxyObject = FreeProxy(country_id=country_id, rand=True)
    headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
    proxy = {"http": proxyObject.get()}
    r = requests.get(url=link, headers=headers, timeout=30, proxies=proxy)
    return parse(r)

def playwright(link):
    from playwright.sync_api import sync_playwright
    import time
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(link)
        print('Waiting for 30s...')
        time.sleep(30)
        r=page.content()
        browser.close()
        return parse(r)
        
        
def ip_scrape(link,IP):
    import requests
    r=requests.get('https://'+str(IP), headers={'host':'youridstore.com.br' }, verify=False)
    
    return parse (r)

''' Method 1 '''

soup=simple_scrape(link)

''' Method 2 '''

headers = {
    'authority': 'www.reddit.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-dest': 'document',
    'accept-language': 'en,en-GB;q=0.9'
}
soup=simple_scrape_header(link,headers)

''' Method 3 '''

soup=cloudscraper_scrape(link)

''' Method 4 '''

soup=selenium_scrape(link)

''' Method 5 '''

soup=proxies_ua_scrape(link,'US')

''' Method 6 '''

soup=playwright(link)


'''Method 7 '''
'''
Get the IP from historical https://securitytrails.com/
Useful for Cloudflare website

'''

soup=ip_scrape('https://youridstore.com.br/tenis-nike-crater-impact-summit-white.html','162.212.57.12')

''' Preview the Soup in HTML '''

preview(soup,'test2')
