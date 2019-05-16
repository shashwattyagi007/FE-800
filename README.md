# FE800 - Risk Analytics Based on Topic Analysis of Financial Disclosures
                                            ######## FOLLOW THESE STEPS ########

Step 1: Run "url_generator.R" in RStudio to get URLs from main SEC webpage containing 
# provide the Ticket of the companies and the year for which you want to get the disclosures for.

Step 2: Now run "scraping_basic.R" in RStudio to scrape the webpage generated from the script in above step
to get the specific URLs for 10-K documents ONLY

Step 3: Now run "scraping_1a_revised.R" in RStudio to extract Section 1A from the Financial Disclosures 
#Uses the URLs from the Step 1 to scrape and store the section 1A text from each 10-K report

Step 4: Run "HDP.py" in Python with the input that is generated in previous step.
# This will give the optimal number of topics that wil be an input in the LDA model

Step : Run "LDA_classifier.py" in Python With the Data from the Step 3 with the optimal number of topics got from Step 4
# This script also contains the Logistic regression model and will classify the rims as risky or not risky
