# Blogging Platform API

## Description
A RESTful API with CRUD operations for a blogging
platform.

## Usage
1. Create a blog: In the url, follow the app route, /api/blog, and use python requests' post method, requests.post, and include the blog user wants to add in the form of a dictionary, json=payload.

```python
import requests # library to call API in python

url = "http://127.0.0.1:5000/api/blog" # make sure route is /api/blog

# example of blog 
payload = {
    "content": "My first blog post!",
    "category": "Programming",
    "tags": ["python", "flask", "backend"]
}

response = requests.post(url, json=payload) # make sure to include json 
print(response.json())
```
2. Update an existing blog: In the URL, follow the app route, /api/blog/<int:id>, and specify the id of the blog you want to update e.g. '/api/blog/<2>'. Use python requests' PUT method, request.put, and include the updated blog that user wants to add, json=payload.

```python
import requests

url = "http://127.0.0.1:5000/api/blog/<2>" # make sure to specify blog id 

# example of a blog
payload = {
    "content": "My first blog post!",
    "category": "Programming",
    "tags": ["python", "flask", "backend"]
}

response = requests.put(url, json=payload) # remember to include json in request and call PUT 
print(response.json())
```

3. Delete an existing blog: In the url, follow the app route, /api/blog/<int:id>, and specify the id of the blog that you wish to delete.Use python requests' DELETE method, requests.delete, and no need to send a json as this is a deletion route.
```python
import requests

url = "http://127.0.0.1:5000/api/blog/<2>" # make sure to specify blog id 

response = requests.delete(url) # no need to include json in request and remember to call DELETE
print(response.json())
```
4. Get a blog by id: In the url, follow the app route, /api/blog/<int:id>, and specify the id of the blog that you wish to get. Use python requests' get method, requests.get, and no need to send a json as this is a get route.

```python
import requests

url = "http://127.0.0.1:5000/api/blog/<2>" # make sure to specify blog id 

response = requests.get(url) # no need to include json in request and remember to call get
print(response.json())
```

5. Get all blogs OR get blogs with specific term: In the url, follow the app route, /api/blog, to get ALL blogs OR specify the term in the form of a query,/api/blog?term=tech, the blogs that you wish to get. Use python requests' get method, requests.get, and no need to send a json as this is a get route.

```python
import requests

url = "http://127.0.0.1:5000/api/blog?term=tech" # make sure to specify the term to get blogs related to the term 

response = requests.get(url) # no need to include json in request and remember to call get
print(response.json())
```

## Installation and running
1. Clone repo
```bash
git clone https://github.com/mdh-danial/blog.git
cd blog
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. run app.py
```bash
python app.py
```
4. Call API (example: Create a blog in a python script)
```python
import requests

url = "http://127.0.0.1:5000/api/blog/post"

payload = {
    "content": "My first blog post!",
    "category": "Programming",
    "tags": ["python", "flask", "backend"]
}

response = requests.post(url, json=payload)
print(response.json())
```

