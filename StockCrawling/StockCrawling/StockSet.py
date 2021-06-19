import pandas as pd
from StockCrawling import Stock, getPrice, setSoup, getCode_DF

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
cnt = 0
# Initialize Stock instance && Set the array for new DataFrame
for name, code in zip(df.name, df.code):
    print(i + 1, cnt +1, sep= "  " )
    i += 1
    stock = Stock(name, code)
    stock.setPrice(getPrice(setSoup(code)))
    subs = stock.getSubs()
    subR = stock.getSubRate()
    if subR <= 2.5: continue

    cnt+=1
    stockName.append(stock.name)
    stockTD.append(stock.getPrice().get("yesterday"))
    stockYS.append(stock.getPrice().get("today"))
    stockSub.append(subs)
    subInfo.append(stock.getSubInfo())
    subRate.append(subR)

# Set new DataFrame of result to save excel file
reDF = pd.DataFrame({
    "종목명": stockName,
    "전일가": stockYS,
    "종가": stockTD,
    "전일대비": subInfo,
    "등락폭": stockSub,
    "등락률": subRate
})
reDF.to_excel("stockInfo2.xlsx", sheet_name="Sheet1")
