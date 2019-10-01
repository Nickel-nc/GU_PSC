#!/usr/bin/env python
# coding: utf-8

# In[24]:


import requests
from getpass import getpass
from pprint import pprint
import json


# In[27]:


# API vk.com manual: https://vk.com/dev/manuals

# https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V
# id225536808
# id token 7138148
# access_token=8068697d35829c90c4854a12e57de00d87835180b7db5a5cf4c5664637eea2d1e72e5557414fbe64308dc&expires_in=0&user_id=225536808

main_link = 'https://api.vk.com/method'
method = 'users.get'
parameters = 'user_ids=225536808&fields=bdate'
token = '8068697d35829c90c4854a12e57de00d87835180b7db5a5cf4c5664637eea2d1e72e5557414fbe64308dc'
V = '5.101'


# In[28]:


req = requests.get(f'{main_link}/{method}?{parameters}&access_token={token}&v={V}')
req.json()

