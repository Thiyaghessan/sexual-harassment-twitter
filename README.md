# Women in Polictics and Misogynistic Twitter Mentions

### Objective
1. Classify tweets containing explicit and implicit misogynistic content 
2. Identify the themes underpinning this content

### Methodology
1. Scrape tweets tagging women in Congress and Senate in the week leading up to the 2020 elections. 
2. Use BERT to classify misogynistic and non-misogynistic twitter mentions
3. Compare both misogynistic and non-misogynistic tweets
4. Perform unsupervised classification (LDA Topic Model) to identify themes in non-misogynistic tweets
5. Communicate results in an interactive dashboard

### Data
We scraped over 400,000 twitter mentions for 146 female senators. A sample of the scraped tweets can be found in "final_data.csv" and the larger file (which was too large to upload on github without git lfs) can be found at https://drive.google.com/file/d/1HLWQuaJzQwqlYYGOHjspKyiQwPAwQK-T/view?usp=sharing. We also used data from Congress.gov and GovTrack USA to conduct further analysis.
All the data used for this project can be found under the "Data" folder, and the raw urls used for to twitter profiles of female senators, and other data can be found under the folder "Scraping tweets -data+code". The trained topic models cab be found under "ldamodels". 

### Code
The code used for the models and data analysis and their respective folders can be found as mentioned below.
1. BERT model : BERT_Classifier_Final.ipynb
2. LDA Topic Model : Topic_Model_Final.ipynb
3. Metadata cleaning : metadata_cleaning.ipynb
4. Word cloud regression : Wordcloud_Regression.ipynb
5. Final data analysis : Final_Project_Analysis.ipynb
6. Dashboard and data visualization : Visualization.ipynb
7. Wordclouds, regression, and LDA topic model weights : util.py
8. Files for Heroku App hosting : requirements.txt, app.py, runtime.txt, Procfile, .gitignore, 
