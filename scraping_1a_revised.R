#load in HTML data..
data = read.csv("url_generator_two.csv", header = TRUE)

#Loading the rvest package
library('rvest')
#Load regex
library(qdapRegex)

text_generator <- function(link){
  #Specifying the url for desired website to be scraped
  url <- link
  
  #Reading the HTML code from the website
  webpage <- read_html(url)
  
  #Using CSS selectors to scrap the rankings section
  actual_html <- html_nodes(webpage,'body') #loads in all text
  
  
  #Converting raw html data to cleaned data
  html_data <- html_text(actual_html)
  
  #extra hard HTML cleansing required
  html_data<- gsub("[\r\n\t]", "", html_data)
  
  #Extract Section 1A
  test <- rm_between(html_data, '1A', '1B', extract=TRUE)#also works!
  test<- paste( unlist(test), collapse='')
  #Test by printing
  return(test)#yayyy!
  
}

#apply function over all 180 links
final_text<- lapply(as.character(data$Link) , text_generator)

#
test_df <- as.data.frame(t(as.data.frame.list(final_text)))
#MANY missing values...#stopped here...
sum(test_df$`test_df$V1` == "NA")
#0 missing!!

#bonus: get rid of row names??
rownames(test_df) <- NULL


test_df<- cbind(data,test_df$V1)

#Last task -- cbind to risk values
risk = read.csv("risk.csv", header = TRUE)

#rename Text 1A columns...
#rename link column
colnames(test_df)[colnames(test_df)=="test_df$V1"] <- "1A_Text"

#drop and keep certain columns
test_df <- test_df[c(3,5:7)]

#revise dates/years
Year<-rep( c("2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"),length(risk))

#testing<- cbind(risk, Year)

#drop old dates
test_df <- test_df[c(2:4)]


#finally merge with year and risk values
test_df<- cbind(Year,test_df,risk)

#Save to disk as a csv and you're done!!!
write.csv(test_df, file = "final_dataframe.csv")



# #check for names of missing companies
# na_test<- subset(test_df,`test_df$V1` == "NA")
# unique(na_test$Ticker)
# #20 missing tickers
# # [1] BA  MMM UNP HON UTX UPS GE  LMT CAT CSX RTN DE  GD  NSC ITW NOC FDX WM  EMR ROP
# 

