from django.test import TestCase

# Create your tests here.

import json

with open('./fixtures/data.json') as f:
    data = json.load(f)


for item in data:
    print(item['name'])
    for i in item['questions']:
        print(i['text'])

