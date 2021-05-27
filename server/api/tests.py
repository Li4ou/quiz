# from django.test import TestCase
#
# # Create your tests here.
import json

with open('main/fixtures/sw_templates.json') as f:
    templates = json.load(f)

print(templates)
