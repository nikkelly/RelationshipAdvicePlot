# TODO: Illustrate M v F age ranges 
# TODO: How to split 23m into 23 and m from [23m] 

import praw
import pandas as pd
import re
from re import search
from creds_ import USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, USER_AGENT

reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USERNAME,password=PASSWORD)

subreddit = reddit.subreddit('relationships')

post_dict = {   'title':[],\
                'url': [],\
                'ageGenderBracket': [],\
                'ageGenderParenth': [],\
                'age': [],\
                'gender': []
                }

n = 0
for submission in subreddit.top(limit=100):
    if search('update', submission.title.lower()):
        pass
    elif (search('\[', submission.title)) or (search('\(', submission.title)):
        post_dict['title'].append(submission.title)
        post_dict['url'].append(submission.url)
        #TODO: might need a loop to go through all matches and put them in seperate rows
        post_dict['ageGenderBracket'].append(re.findall(r'\[(.*?)\]', submission.title))
        post_dict['ageGenderParenth'].append(re.findall(r'\((.*?)\)',submission.title))
        post_dict['age'].append(re.findall(r'\d+', str(post_dict['ageGender'][n]))) 
        post_dict['gender'].append(re.findall(r'[mfMF]', str(post_dict['ageGender'][n]))) 
        n += 1
else:
        pass

post_df = pd.DataFrame(post_dict)
#save to CSV to debug
post_df.to_csv('FILENAME.csv', index=False)

print(post_df['age'][8] + post_df['gender'][8])