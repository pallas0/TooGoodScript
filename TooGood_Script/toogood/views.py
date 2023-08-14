from django.shortcuts import render
from config import client
import requests

# Create your views here.
#third party API calls go here
items = client.get_items()
print(items)