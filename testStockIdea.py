import ystockquote
import pprint
import sys
import csv
import time
from datetime import datetime, timedelta
import sqlite3
db = sqlite3.connect('test.db')
cursor = db.cursor()

tradesCols = ["tradeID", "date", "action", "stockName", "sharesAmount", "price"]
stocksCols = ["stockName", "industry", "market", "keywords"]
stockInfoCols = ["stockName", "time", "price", "fifty_two_week_low", 
	"price_earnings_ratio", "earnings_per_share", "avg_daily_volume", 
	"ebitda", "market_cap", "volume", "price_earnings_growth_ratio", 
	"book_value", "change", "two_hundred_day_moving_avg", "price_sales_ratio", 
	"fifty_two_week_high", "fifty_day_moving_avg", 
	"price_book_ratio", "dividend_yield", "dividend_per_share", "short_ratio"]
	

def setupTables():
	cursor.execute("create table if not exists trades ('tradeID','date','action','stockName','sharesAmount','price')")
	cursor.execute("create table if not exists stocks ('stockName', 'industry','market','keywords')")
	cursor.execute("create table if not exists stockInfo ('id' INTEGER PRIMARY KEY, 'stockName', 'time', 'price', 'fifty_two_week_low', 'price_earnings_ratio', 'earnings_per_share', 'avg_daily_volume', 'ebitda', 'market_cap', 'volume', 'price_earnings_growth_ratio', 'book_value', 'change', 'two_hundred_day_moving_avg', 'price_sales_ratio', 'fifty_two_week_high', 'fifty_day_moving_avg', 'price_book_ratio', 'dividend_yield', 'dividend_per_share', 'short_ratio')")

def getAllStocksInfo():
	startTime = time.time()
	symbols = getStockSymbols()
	for symbol in symbols:
		info = ygetAllStockInfo(symbol[0])
		info["symbol"] = symbol[0]
		daddStockInfo(info);
	elapsedTime = time.time() - startTime
	print('Total runtime = ' + "{:.9f}".format(elapsedTime))
	
def ygetPrice(stockName):
	return ystockquote.get_price(stockName)
	
def ygetHistorical(stockName, startDate, endDate):
	return ystockquote.get_historical_prices(stockName, startDate, endDate)
	
def ygetAllStockInfo(stockName):
	print(stockName)
	return ystockquote.get_all(stockName)
	
def getStockSymbols():
	stockSymbols = []
	symbolReader = csv.reader(open('NYSE.csv', 'r'),quoting=csv.QUOTE_NONE, skipinitialspace=True)
	for row in symbolReader:
		stockSymbols.append(row)
	return stockSymbols

def dgetAllStocks():
	cursor.execute("SELECT * FROM stocks")
	print(cursor.fetchall())

def daddStock():
	cursor.execute("INSERT INTO stocks VALUES (?,?,?,?)", symbol, industry, market, keyword);
	db.commit()

def daddStocks(stocks):
	cursor.executemany("INSERT INTO stocks VALUES (?,?,?,?)", stocks)

def daddStockInfo(stockInfo):
	curTime = time.time();
	propsArray = [
		None,
		stockInfo["symbol"], 
		curTime,  
		stockInfo["price"],
		stockInfo["fifty_two_week_low"],
		stockInfo["price_earnings_ratio"],
		stockInfo["earnings_per_share"],
		stockInfo["avg_daily_volume"],
		stockInfo["ebitda"],
		stockInfo["market_cap"],
		stockInfo["volume"],
		stockInfo["price_earnings_growth_ratio"],
		stockInfo["book_value"],
		stockInfo["change"],
		stockInfo["two_hundred_day_moving_avg"],
		stockInfo["price_sales_ratio"],
		stockInfo["fifty_two_week_high"],
		stockInfo["fifty_day_moving_avg"],
		stockInfo["price_book_ratio"],
		stockInfo["dividend_yield"],
		stockInfo["dividend_per_share"],
		stockInfo["short_ratio"]
	]
	cursor.execute("INSERT INTO stockInfo VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", propsArray)
	db.commit()

def daddAction(date, action, stockName, sharesAmount, price):
	#verify data coming in is of right type
	cursor.execute("INSERT INTO trades VALUES (?,?,?,?,?)", (date, action, stockName, sharesAmount, price))
	db.commit()

def daddActions(actionArray):
	#verify actionArray is of right types
	cursor.executemany("INSERT INTO stocks VALUES (?,?,?,?,?)", actionArray)

def dgetStock(stockName):
	stockInfo = cursor.execute("SELECT * FROM stocks WHERE stockName=?", stockName)
	print(stockInfo)

def dgetStockInfo(stockName):
	stockInfo = cursor.execute("SELECT * FROM stockInfo WHERE stockName=?", stockName)
	print(stockInfo)

def dgetAllStockInfo():
	cursor.execute("SELECT * FROM stockInfo")
	stocks = cursor.fetchall()
	for stock in stocks:
		print(stock)

def closeDB():
	db.close()

def dgetTradeInfo(tradeID):
	tradeInfo = cursor.execute("SELECT * FROM trades WHERE tradeID=?", tradeID)
	print(tradeInfo)

def dgetTradesByDate(date):
	tradeInfo = cursor.execute("SELECT * FROM trades WHERE date=?", date)
	print(tradeInfo)

def dgetTradesByDateAndStock(date, stockName):
	tradeInfo = cursor.execute("SELECT * FROM trades WHERE date=? AND stockName=?", (date, stockName))
	print(tradeInfo)
	
if __name__ == "__main__":
	setupTables()
	getAllStocksInfo()
	#dgetAllStockInfo()