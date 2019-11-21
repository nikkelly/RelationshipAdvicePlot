# TODO: Illustrate M v F age ranges 
# TODO: Figure out how to drop rows with blank ageGenders
# TODO: How to split 23m into 23 and m from [23m] 
# Test Regex here: https://www.regextester.com/21
# Regex Tries: 
# 23
# 23m 
# [23]
# [23m]
# [23 m]
# [23 M]
# [23M]
# 23f
# [23]
# [23f]
# [23 f]
# [23 f]
# [23f]

import praw
import pandas as pd
import re
from re import search

reddit = praw.Reddit(client_id='K0KrmkKEnFy9Nw',client_secret='GyPJvZsBH-HQgHzY16PkwXL1E_M',user_agent='relationshipScrape',username='relationshipscrape',password='plottingarelationship')

subreddit = reddit.subreddit('relationships')

post_dict = { 'title':[],\
                'url': [],\
                'bracket': [],\
                'parenth':[],\
                }

#Brackets
regexBracket = re.compile(r'\[(.*?)\]') #! Working
regexParenth = re.compile(r'\((.*?)\)') #! Working
regexAge = re.compile(r'\d')
regexGender = re.compile(r'[a-zA-Z]')

for submission in subreddit.top(limit=100):
    if search('update', submission.title.lower()):
        pass
    else:
        post_dict['title'].append(submission.title)
        post_dict['url'].append(submission.url)
        post_dict['bracket'].append(re.findall(regexBracket,submission.title))
        post_dict['parenth'].append(re.findall(regexParenth, submission.title))

post_dictdf = pd.DataFrame(post_dict)
post_dictdf['ageGender'] = post_dictdf['bracket'] + post_dictdf['parenth']

# Delete unused columns
post_dictdf.pop('bracket')
post_dictdf.pop('parenth')
#save to CSV 
post_dictdf.to_csv('FILENAME.csv', index=False)

#TODO
for index,rows in enumerate(post_dictdf.ageGender):
    if len(rows) == 0:
        print(index,rows)
        print(post_dictdf['title'][index])

post_dictdf.to_csv('testfile.csv', index=False)
