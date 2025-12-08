# Learning points

## What is CRUD?
CRUD stands for Create, Read, Update, Delete

## client sending a JSON to API
The API only accepts JSON as a request from the client. Thus, the API call of client looks as such:
```python
import requests

url = "http://127.0.0.1:5000/api/blogs"

payload = {
    "content": "My first blog post!",
    "category": "Programming",
    "tags": ["python", "flask", "backend"]
}

response = requests.post(url, json=payload)
print(response.json())
```

- this sends a POST request to the designated route (/api/blogs) with a json (json=payload)

app.py then receives the data accordingly:
```python
from flask import request, jsonify

data = request.get_json()
content = data.get("content") # gets value from "content" key
category = data.get("category") # gets value from "category" key
tags = data.get("tags", []) # default empty list

# return json message 
return jsonify({"message": "Blog created successfully"}), 201
