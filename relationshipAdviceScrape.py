# TODO: Illustrate M v F age ranges 
# TODO: How to split 23m into 23 and m from [23m] 
#! Current problems:
#! ageGender shows a tuple(?) inside of the column

import praw
import pandas as pd
import re
from re import search
from creds_ import USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, USER_AGENT
from matplotlib import pyplot as plt

reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USERNAME,password=PASSWORD)

subreddit = reddit.subreddit('relationships')

post_dict = {   'title':[],\
                'url': [],\
                'ageGenderBracket': [],\
                'ageGenderParenth': [],\
                'ageBracket': [],\
                'genderBracket': [],\
                'ageParenth': [],\
                'genderParenth': [],\
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
        # Seperate brackets
        post_dict['ageBracket'].append(re.findall(r'\d+', str(post_dict['ageGenderBracket'][n]))) 
        post_dict['genderBracket'].append(re.findall(r'[mfMF]', str(post_dict['ageGenderBracket'][n]))) 
        # Seperate Partenth
        post_dict['ageParenth'].append(re.findall(r'\d+', str(post_dict['ageGenderParenth'][n]))) 
        post_dict['genderParenth'].append(re.findall(r'[mfMF]', str(post_dict['ageGenderParenth'][n]))) 
        n += 1
else:
        pass

post_df = pd.DataFrame(post_dict)
# Combine age and gender columns 
post_df['age'] = post_df['ageParenth'] + post_df['ageBracket']
post_df['gender'] = post_df['genderParenth'] + post_df['genderBracket']

# Combine all the lists into one big list for Age
allAges = []
rowNumber = 0
for rows in post_df['age']:
        allAges += post_df['age'][rowNumber]
        rowNumber += 1
# Repeat for Gender
allGenders = []
rowNumber = 0
for rows in post_df['gender']:
        allGenders += post_df['gender'][rowNumber]
        rowNumber += 1
allGenders = [x.upper() for x in allGenders]

ageGender_df = pd.DataFrame()
ageGender_df['age'] = allAges
ageGender_df['gender'] = allGenders
ageGender_df['age'] = ageGender_df['age'].astype('int')

# Plot it all
fix, axes = plt.subplots(nrows=2, ncols=2)

plt.subplot(3,1,1)
plt.xlabel('Age')
plt.ylabel('Count of Age')
plt.plot(ageGender_df['age'])

plt.subplot(3,1,2)
plt.xlabel('Gender')
plt.ylabel('Count of Gender')
plt.hist(ageGender_df['gender'])

plt.show()