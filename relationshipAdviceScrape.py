
#! PRAW Doesn't allow more than 1k submissions per request. 
#! this needs to be done through pushshift.io

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
for submission in subreddit.hot(limit=None):
    if search('update', submission.title.lower()):
        pass
    elif (search('\[', submission.title)) or (search('\(', submission.title)):
        post_dict['title'].append(submission.title)
        post_dict['url'].append(submission.url)
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

#!Start Debug
#TODO: Figure out how to get more than ~500 submissions 
#* Probably need to loop through and pull by UTC submission time
test_dict = {
        'submission': [],\
        'createdUTC': [],\
}
for submission in subreddit.new(limit=10,):
        test_dict['submission'].append(submission.id)
        test_dict['createdUTC'].append(submission.created_utc)
test_df = pd.DataFrame(test_dict)
test_df.to_csv('test_df.csv',index=False)
print('Total Submissions(dict): '+str(len(test_dict)))
print('Total Submissions(df): '+str(range(test_df)))
print('Starting with '+str(len(post_df))+' total lines')
#!End Debug

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

age_df = pd.DataFrame()
gender_df = pd.DataFrame()

age_df['age'] = allAges
age_df['age'].fillna('999')
gender_df['gender'] = allGenders
ageGender_df = pd.DataFrame()
ageGender_df['age'] = age_df['age']
ageGender_df['gender'] = gender_df['gender'].astype('str')
ageGender_df['gender'] = ageGender_df['gender'].fillna('N/A')
ageGender_df['age'] = ageGender_df['age'].astype('int')

#!Start Debug
# rowNumber = 0 
# for line in ageGender_df['age']:
#         if '45' in line:
#                 print(str(ageGender_df['age'][rowNumber])+str(ageGender_df['gender'][rowNumber]))
#         rowNumber +=1
# ageGender_df.to_csv('ageGender.csv',index=False)
# print(ageGender_df.dtypes)
#!End Debug

# Plot it all
fix, axes = plt.subplots(nrows=2, ncols=2)

plt.subplot(2,1,1)
plt.title('Age Distribution of /r/relationships')
plt.xlabel('Age')
plt.ylabel('Count of Age')
plt.hist(ageGender_df['age'])

plt.subplot(2,1,2)
plt.xlabel('Gender')
plt.ylabel('Count of Gender')
plt.hist(ageGender_df['gender'])

plt.show()