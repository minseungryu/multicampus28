import requests
from bs4 import BeautifulSoup
import pandas as pd

com_codes = ["030200", "005930"]
com_names = ["KT", "삼성전자"]
com_price = []

def makeDf(all_list):
    df = pd.DataFrame({"code":com_codes, "name": com_names, "price": com_price})
    return df

def crawler(soup):
    price = soup.find("div", class_="today").find ("span", class_="blind")
    com_price.append(price.text)
    return None

def main():   
    custom_header = {
        'referer' : 'https://finance.naver.com/item/main.naver?',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    main_url = "https://finance.naver.com/item/main.naver?"

    for i in com_codes:
        url = main_url+"code="+i
        req = requests.get(url, headers = custom_header)
        soup = BeautifulSoup(req.text, "html.parser")
        result = crawler(soup)
    
    final_df = makeDf(result)
    return  print(final_df)

if __name__ == "__main__":
    main()

"""
1. 코드번호 가져오기
2. for i in [코드번호]:
    url = "~/000000"
"""