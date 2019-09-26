#!/usr/bin/env python
# coding: utf-8

# In[26]:


import requests
from getpass import getpass
from pprint import pprint
import json


# In[92]:


# API github manual: https://developer.github.com/v3/

username = 'Nickel-nc'
repo_owner = 'Yorko'
password = getpass()
main_link = 'https://api.github.com'
req = requests.get(f'{main_link}/users/{repo_owner}/repos', auth = (username, password))
data = json.loads(req.text)

lst = []
for i in range(len(data)):
    lst.append(data[i]['name'])
lst


# In[106]:


s = json.dumps(lst)
s1 = json.loads(s)


# In[109]:


with open('HW_1.1_response.json', 'w', encoding='utf-8') as file:
    json.dump(s1, file, indent=2, ensure_ascii=False)


# In[ ]:




