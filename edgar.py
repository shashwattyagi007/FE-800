# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:43:05 2019

@author: Jean Martin Guest
"""
#import package
import sec_edgar_downloader

#specify directory for downloaded 10-K files to be saved into
#if left blank the function will search for the user's 'Downloads" folder
downloader = sec_edgar_downloader.Downloader(r"C:\Users\Jean Martin Guest\Downloads\SEC_Test")

#Create function to download 10K filing for the last 9 years (2010-2018)
def file_downloader(*argv):
    for arg in argv:
        downloader.get_10k_filing_for_ticker(arg, 9)

# Get the last 10-K filings for each company by ticker, for the top 20 companies in the S&P 500 IT sector
file_downloader('MSFT', 'APPL', 'GOOGL',  'FB', 'V', 'INTC', 'MA', 'CSCO', 'ORCL', 'ADBE', 'CRM', 'IBM', 'ACN', 'TXN', 'NVDA', 'QCOM', 'ADP', 'INTU', 'MU', 'CTSH')

