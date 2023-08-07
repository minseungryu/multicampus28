# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

def main():
    # index.html을 불러와서 BeautifulSoup 객체 초기화
    # 웹에서 응답을 할 때, html, xml, json 등 여러가지 방식이 존재함
    # 메서드 여러가지 사용해보기
    soup = BeautifulSoup(open("html/index.html", encoding="utf-8"), "html.parser")
    print(type(soup))
    print(soup.title)

    print(soup.title.string)
    print(soup.find("p").get_text())

    fake_str = soup.find('div', class_='fakecampus').find_all('p')
    print(fake_str[2].get_text())


if __name__ == "__main__":
    main()

