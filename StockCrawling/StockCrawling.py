import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook


# Stock 클래스
class Stock:
    price = {}
    ysPrice = 0
    tdPrice = 0

    def __init__(self, name, code):  # 외부 주입 by KRX 전체 종목 xlsx 파일
        self.name = name  # 종목명
        self.code = code  # 종목 코드

    # Set Price from crawling
    def setPrice(self, price):
        self.price = price  # Dictionary (Hashmap) type

    # Get Price dictionary
    def getPrice(self):
        return self.price

    # Get 등락폭 계산
    def getSubs(self):
        price_td = ""
        price_ys = ""
        for td, ys in zip(self.price.get("today"), self.price.get("yesterday")):
            if td != ",":  price_td += td
            if ys != ",": price_ys += ys
            self.ysPrice = int(price_ys)
            self.tdPrice = int(price_td)

        return self.tdPrice - self.ysPrice

    # Get 등락비
    def getSubInfo(self):
        if self.tdPrice - self.ysPrice < 0:
            return "하락"
        elif self.tdPrice - self.ysPrice > 0:
            return "상승"
        else:
            return "--"

    # Get 등락률
    def getSubRate(self):
        if self.ysPrice == 0: return 0
        return (abs(self.tdPrice - self.ysPrice) / self.ysPrice) * 100


# KRX 전체 종목 : 종목코드 Crawling
# Get Name & Code Pandas DataFrame
def getCode_DF():
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    df.종목코드 = df.종목코드.astype(str).apply(lambda x: x.zfill(6))
    df = df[['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    return df


# Soup html parsing
def setSoup(code):
    html = requests.get("https://finance.naver.com/item/main.nhn?code=" + code).text

    return BeautifulSoup(html, 'html.parser')


# 전일가, 종가, Crawling
def getPrice(soup):
    price = {"yesterday": "", "today": ""}
    # price["low"] = soup.find('em', {"class": "no_down"}).find("span", {"class": "blind"}).text
    # price["high"] = soup.find('em', {"class": "no_up"}).find("span", {"class": "blind"}).text
    price["yesterday"] = soup.find('td', {"class": "first"}).find("span", {"class": "blind"}).text
    price["today"] = soup.find('p', {"class": "no_today"}).find("span", {"class": "blind"}).text

    return price


# Start Setting DataFrame for Crawling here
df = getCode_DF()
stockArr = []
stockName = []
stockTD = []
stockYS = []
stockSub = []
subInfo = []
subRate = []
i = 0

# Initialize Stock instance && Set the array for new DataFrame
for name, code in zip(df.name, df.code):
    if i >= 1500: break
    print(i + 1)
    stockArr.append(Stock(name, code))
    stockArr[-1].setPrice(getPrice(setSoup(code)))
    stockArr[-1].getSubs()

    stockName.append(stockArr[-1].name)
    stockTD.append(stockArr[-1].getPrice().get("yesterday"))
    stockYS.append(stockArr[-1].getPrice().get("today"))
    stockSub.append(stockArr[-1].getSubs())
    subInfo.append(stockArr[-1].getSubInfo())
    subRate.append(stockArr[-1].getSubRate())
    i += 1

# Set new DataFrame of result to save excel file
reDF = pd.DataFrame({
    "종목명": stockName,
    "전일가": stockYS,
    "종가": stockTD,
    "전일대비": subInfo,
    "등락폭": stockSub,
    "등락률": subRate
})
reDF.to_excel("stockInfo.xlsx", sheet_name="Sheet1")
