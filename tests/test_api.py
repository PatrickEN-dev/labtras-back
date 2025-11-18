#!/usr/bin/env python3
import requests
import json

try:
    response = requests.get("http://localhost:8000/api/rooms/")
except Exception as e:
    pass
