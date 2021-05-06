#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:31:07 2021

@author: allie
"""

# ML Final 

from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd

# BAC - Bank of America Coporation - financial
# BA - Boeing Company - industrial manufactoring
#  MDLZ - Mondelez International Inc. - consumer goods
#  PFE - Pfizer - health care 
# GOOG -  Tech industry
ticker_list = ['BAC', 'BA', 'GOOG', 'MDLZ', 'PFE']


# get historical time series data for stocks 
historical_datas = {}

for ticker in ticker_list:
    historical_datas[ticker] = get_data(ticker)

stock_data = pd.concat(historical_datas)


income = {}
balance = {}
cash = {}

for ticker in ticker_list: 
    income_statement = si.get_income_statement(ticker)
    inc_transposed = income_statement.transpose()
    income[ticker] = inc_transposed
    balance_statement = si.get_balance_sheet(ticker)
    bal_transposed = balance_statement.transpose()
    balance[ticker] = bal_transposed
    cash_statement = si.get_cash_flow(ticker)
    cash_transposed = cash_statement.transpose()
    cash[ticker] = cash_transposed
    
income = pd.concat(income)
balance = pd.concat(balance)
cash = pd.concat(cash)
   
financials = pd.concat([income, balance, cash], axis = 1)

# get data for american indices 
sp = get_data('^GSPC')
dow = get_data('^DJI')

# clean stock data
stock_data.reset_index(inplace = True)
stock_data = stock_data.rename(columns = {'level_1': 'Date'})
stock_data = stock_data.drop(columns = ['level_0'])
stock_data['Date']= stock_data['Date'].dt.date

# clean sp and dow 
sp.reset_index(inplace = True)
dow.reset_index(inplace = True)
sp = sp.rename(columns = {'index': 'Date'})
dow = dow.rename(columns = {'index': 'Date'})
sp['Date']= sp['Date'].dt.date
dow['Date']= dow['Date'].dt.date

sp = sp.rename( columns = {'high':'S&P500'})
dow = dow.rename(columns = {'high': 'DowJones'})
sp = sp[['Date', 'S&P500']]
dow = dow[['Date', 'DowJones']]

# filter out data from before 2017
stock_data['Year']=stock_data['Date'].apply(lambda x: x.year)
sp['Year']=sp['Date'].apply(lambda x: x.year)
dow['Year']=dow['Date'].apply(lambda x: x.year)

stock_data = stock_data[stock_data['Year']>=2017]
sp = sp[sp['Year']>=2017]
dow = dow[dow['Year']>=2017]
stock_data = stock_data.drop(columns = ['Year'])
sp = sp.drop(columns = ['Year'])
dow = dow.drop(columns = ['Year'])

data = stock_data.merge(sp, how ='left', on = 'Date')
data = data.merge(dow, how = 'left', on = 'Date')

# prepare financials data 
financials.reset_index(inplace = True)
financials = financials.rename(columns = {'endDate':'Year', 'level_0':'ticker'})
financials['Year'] = financials['Year'].apply(lambda x: x.year)
# merge with financial data 
data['Year']= data['Date'].apply(lambda x: x.year)
data = data.merge(financials, how = 'left', on = ['Year', 'ticker'])
data = data.drop(columns = ['Year'])

data.to_csv("/Users/allie/Desktop/Universität/Master/data.csv")