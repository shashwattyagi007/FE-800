#URLs generator

#Load libraries

library(edgarWebR)
library(knitr)

#Create function

####################
#Find a Submission
# ticker <- "STX"
# 
# filings <- company_filings(ticker, type = "10-K", count = 40)
# # Specifying the type provides all forms that start with 10-, so we need to
# # manually filter.
# filings <- filings[filings$type == "10-K", ]
# 
# # We're only interested in the last nine reports so...
# filings <- head(filings,9)
# filings <-  data.frame(filings$filing_date, filings$href)
# names(filings) <- c("Date", "HTML Link")
# filings$Ticker <- ticker
###########################

url_generator <- function(ticker) {
  filings <- company_filings(ticker, type = "10-K", count = 40)
  # Specifying the type provides all forms that start with 10-, so we need to
  # manually filter.
  filings <- filings[filings$type == "10-K", ]
  
  #filter by date
  filings$filing_date <- as.Date(filings$filing_date, format= "%Y-%m-%d")
  #filings<- subset(filings, filing_date> "2010-01-01" & filing_date < "2018-12-31")
  filings<- subset(filings, filing_date> "2010-07-01" & filing_date < "2019-12-31")
  
  #rename columns
  filings <-  data.frame(filings$filing_date, filings$href)
  names(filings) <- c("Date", "HTML Link")
  filings$Ticker <- ticker
  return(filings)
}

list <- c('BA', 'MMM', 'UNP', 'HON', 'UTX', 'UPS', 'GE', 'LMT', 'CAT', 'CSX', 'RTN', 'DE', 'GD', 'NSC', 'ITW', 'NOC','FDX', 'WM', 'EMR', 'ROP')

final<- rbind(url_generator('BA'), url_generator('MMM'),url_generator('UNP'),url_generator('HON'), url_generator('UTX'),url_generator('UPS'), url_generator('GE'),url_generator( 'LMT'),url_generator( 'CAT'),url_generator( 'CSX'),url_generator( 'RTN'),url_generator( 'DE'),url_generator( 'GD'),url_generator( 'NSC'),url_generator( 'ITW'), url_generator('NOC'),url_generator('FDX'),url_generator( 'WM'),url_generator( 'EMR'),url_generator( 'ROP'))

write.csv(final, file = "url_generator.csv")



