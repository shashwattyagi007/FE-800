#load in HTML data..
data = read.csv("url_generator.csv", header = TRUE)

#Loading the rvest package
library('rvest')

reports <- function(link){
  #Specifying the url for desired website to be scraped
  url <- link
  
  #Reading the HTML code from the website
  webpage <- read_html(url)
  
  #Using CSS selectors to scrap the rankings section
  actual_html <- html_nodes(webpage,'td')
  
  #Converting the ranking data to text
  html_data <- html_text(actual_html)
  
  #Let's have a look at the rankings
  head(html_data)
  path<- html_data[3] #gives specific url
  
  build <- sub('/([^/]*)$', "", url)
  new_url<- paste(build,'/',path)
  new_url<- gsub(" ", "", new_url, fixed = TRUE)
  return(new_url) #this is the url needed!
  
}

#print(as.character(data$HTML.Link[1]))
#print(as.character(data$HTML.Link[]))



#final_links<- rbind(reports(as.character(data$HTML.Link[1])))
#works ok

#dumbass hours are all hours yeehaw
#final_links<- rbind(reports(as.character(data$HTML.Link[])))

final_links_test<- lapply(as.character(data$HTML.Link) , reports)

test <- as.data.frame(t(as.data.frame.list(final_links_test)))
#final_links_test <- as.data.frame(final_links_test) #mistakes!

test_two<- cbind(data,test$V1)

#fix HTML errors #NEW
test_two$`test$V1`<-gsub("(htm).*","\\1",test_two$`test$V1`)


#rename link column
colnames(test_two)[colnames(test_two)=="test$V1"] <- "Link"

#write to csv
write.csv(test_two, file = "url_generator_two.csv")

#bonus: get rid of row names??
rownames(test_two) <- NULL
#shit it works ok


#df <- test_two[ -c(1) ]

###########################################


# #Specifying the url for desired website to be scraped
# url <- 'https://www.sec.gov/Archives/edgar/data/1137789/000119312517248796/0001193125-17-248796-index.htm'
# 
# #Reading the HTML code from the website
# webpage <- read_html(url)
# 
# 
# #Using CSS selectors to scrap the rankings section
# actual_html <- html_nodes(webpage,'td')
# 
# 
# #Converting the ranking data to text
# html_data <- html_text(actual_html)
# 
# #Let's have a look at the rankings
# head(html_data)
# path<- html_data[3] #gives specific url
# 
# build <- sub('/([^/]*)$', "", url)
# new_url<- paste(build,'/',path)
# new_url<- gsub(" ", "", new_url, fixed = TRUE)
# print(new_url) #this is the url needed!
# 
# #okay now we need the regex....
# 
# 
