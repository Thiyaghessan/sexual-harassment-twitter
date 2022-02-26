! pip install twint

! pip uninstall twint

! pip install nest_asyncio

! pip3 install --user --upgrade "git+https://github.com/twintproject/twint.git@origin/master#egg=twint"

! /Users/pranathiiyer/opt/anaconda3/bin/python -m pip install --upgrade pip

! pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

! pip3 install twint

import pandas as pd
user_names = []
urls = pd.read_csv('raw_urls.txt', header= None)
for url in urls[0]:
    user_names.append('@'+url.split('/')[3].split('?')[0].replace('\xa0',''))
data[0] = user_names
final_df = pd.DataFrame(columns = ['id','conversation_id','candidate_user_name','date','tweet','pol_party','targetted_comment'])
import twint
import nest_asyncio
nest_asyncio.apply()
for user,party in data[6:].itertuples(index = False):
    
    try:
        
        c = twint.Config()
        c.Lang = "en"
        c.Search = user
        c.Since = '2020-10-27'
        c.Hide_output = True
        c.Until= '2020-11-02'
        c.Pandas= True
        twint.run.Search(c)
        test_df = twint.storage.panda.Tweets_df
        targetted_comment = []

        for i in test_df['reply_to']:

            if i== []:

                targetted_comment.append('N')   
            else:
                tar_reply = False
                for dct in i:

                    if dct['screen_name'] == user[1:]:
                        tar_reply = True

                        break
                if tar_reply:
                     targetted_comment.append('Y')
                else:
                     targetted_comment.append('N')

        test_df['targetted_comment'] = targetted_comment

        processed_tweets = []
        for tweet in test_df['tweet']:
            processed_tweets.append(" ".join(filter(lambda x:x[0]!='@', tweet.split())))

        test_df['tweet'] = processed_tweets
        test_df.drop(test_df.loc[test_df['language'] != 'en'].index, inplace=True)
        candidate = [user[1:]]*len(test_df)
        pol_party = [party]*len(test_df)
        test_df['candidate_user_name'] = candidate
        test_df['pol_party'] = pol_party


        final_df = final_df.append(test_df[['id','conversation_id','candidate_user_name','date','tweet','pol_party','targetted_comment']])
        
    except:
        continue

final_df.to_csv('/Users/pranathiiyer/Desktop/cs_project_data/final_data_1.csv',index = False)    
            
            
           
            
               