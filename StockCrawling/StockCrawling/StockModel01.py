import requests
from bs4 import BeautifulSoup
import pandas as pd


# Get 52-Highest Price  ( Naver Crawling)
def getHighest(code):
    high = BeautifulSoup(requests.get("https://finance.naver.com/item/main.nhn?code=" + code).text, 'html.parser').find(
        'table', {'class': 'rwidth'}).select("td > em")[1]
    return high


# Get Date & Price during 100 days (Yahoo-finance Crawling)
def setSoup(code):
    url = "https://finance.yahoo.com/quote/005930.KS/history?p=" + code + ".KS"
    return BeautifulSoup(requests.get(url).text, 'html.parser').find("table", {"class": "W(100%) M(0)"}).findAll("span")


# Date, Price parsing
def get_all_price(soup):
    cnt = 0

    # Date Parsing - Inner Function
    def parsing_date(textDate):

        temDate = ""
        for temD in textDate:
            if temD == ",": break
            temDate += temD

        return temDate

    # Price Parsing - Inner Function
    def parsing_price(textPrice):

        temPrice = ""
        for temP in textPrice:
            if temP == ".": break
            if temP == ",": continue
            temPrice += temP
        try:
            temPrice = int(temPrice)
        except:
            pass

        return temPrice

    # get_all_price & date function starts from here
    for tag in soup:
        cnt += 1
        if tag.get_text() == "Dividend":
            cnt += 5
            date.pop()
        elif cnt % 7 == 1:
            if tag.get_text() == "Date": continue
            date.append(parsing_date(tag.get_text()))
        elif cnt % 7 == 2:
            if tag.get_text() == "Open": continue
            price.append(parsing_price(tag.get_text()))
    price.pop()
    date.pop()


date = []
price = []
code = "051910"
get_all_price(setSoup(code))

df = pd.DataFrame({
    "Date":date,
    "Price":price
})

# print(df)
# for d, p in zip(date, price): print(d, p, sep=", ")