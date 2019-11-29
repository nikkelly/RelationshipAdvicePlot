
#TODO: Right now it doesn't read info the right way 
#TODO: Figure out how to import the CSV and read through each line of it. 
import requests
from datetime import datetime
import traceback
import re
from re import search
import pandas as pd

username = 'relationshipscrap3'

url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=relationships&before='
start_time = datetime.utcnow()

def downloadFromURL(filename):
  print(f'saving to {filename}')
  count = 0
  handle = open(filename, 'w')
  previous_epoch = int(start_time.timestamp())
  while True:
    new_url = url.format()+str(previous_epoch)
    json = requests.get(new_url, headers={'User-Agent' : 'relationshipscrape'})
    json_data = json.json()
    if 'data' not in json_data:
      break
    objects = json_data['data']
    if count == 100:
      break
    if len(objects) == 0:
      break

    for object in objects:
      previous_epoch = object['created_utc'] - 1
      count += 1
      if object['is_self']:
        if 'selftext' not in object:
          continue
        try:
          handle.write(object['title'].lower())
          handle.write('\n')
          # text = object['selftext']
          # textASCII = text.encode(encoding='ascii', errors='ignore').decode()
        except Exception as err:
          print('Couldn\'t print post: '+object['url'])
          print(traceback.format_exc())
    print('saved {} submissions through {}'.format(count, datetime.fromtimestamp(previous_epoch).strftime('%Y-%m-%d')))
  print(f'Saved {count}')
  handle.close()

def findAgeGender(filename):
  post_dict = {   'title':[],\
                'url': [],\
                'ageGenderBracket': [],\
                'ageGenderParenth': [],\
                'ageBracket': [],\
                'genderBracket': [],\
                'ageParenth': [],\
                'genderParenth': [],\
                }
  print(f'Opening {filename}')
  count = 0 
  for row in filename:
    if search('update', row.lower()):
      pass
    else:
      post_dict['ageGenderBracket'].append(re.findall(r'\[(.*?)\]',row))
      post_dict['ageGenderParenth'].append(re.findall(r'\((.*?)\)',row))
      print(row)
      # Seperate brackets
      post_dict['ageBracket'].append(re.findall(r'\d',str(post_dict['ageGenderBracket'][count])))
      post_dict['genderBracket'].append(re.findall(r'[mf]', str(post_dict['ageGenderBracket'][count])))
      # Seperate parenths
      post_dict['ageParenth'].append(re.findall(r'\d',str(post_dict['ageGenderParenth'][count])))
      post_dict['genderParenth'].append(re.findall(r'[mf]', str(post_dict['ageGenderParenth'][count])))
      count += 0
      post_dict['age'] = post_dict['ageParenth'] + post_dict['ageBracket']
      post_dict['gender'] = post_dict['genderParenth'] + post_dict['genderBracket']
  # Combine all the lists into one big list for Age
  allAges = []
  rowNumber = 0
  for rows in post_dict['age']:
          allAges += post_dict['age'][rowNumber]
          rowNumber += 1
  # Repeat for Gender
  allGenders = []
  rowNumber = 0
  for rows in post_dict['gender']:
          allGenders += post_dict['gender'][rowNumber]
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
  
  #! Start Debug
  csvFilename = 'ageGender_df(requests).csv'
  ageGender_df.to_csv(csvFilename, index=False)
  print(f'Saved all posts Ages and Genders to: {csvFilename}' )
  print(allAges)
  print(gender_df.head())
  #! End Debug

# downloadFromURL('posts.csv')
findAgeGender('posts.csv')