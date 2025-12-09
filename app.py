from flask import Flask, request, jsonify
import sqlite3
import re

# tell flask the root file (app.py)
app = Flask(__name__)

def normalize_tag(tag: str) -> str:
    tag = tag.strip().lower()
    tag = re.sub(r'[^a-z0-9]+', '', tag)
    return tag

def get_db():
    conn = sqlite3.connect('blogs.db') # Connect to your database
    conn.row_factory = sqlite3.Row # To return rows as dictionaries
    return conn

def create_table():
    """Create tables if it doesn't exist"""

    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            createdAt DATE DEFAULT (DATE('now')),
            updatedAt DATE DEFAULT (DATE('now'))
        );
                    
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
                    
        CREATE TABLE IF NOT EXISTS blog_tags (
            blog_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (blog_id, tag_id),
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        );                
    """)
    conn.close()

# create route
@app.route("/api/blog/post", methods=["POST"])
def create_post():

    # obtain data from request
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "Bad request"}), 400

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    tags = data.get("tags", [])  # list of strings
    
    # validate keys from JSON request 
    if not title or not isinstance(title, str):
        return jsonify({"message":"Must be valid title"}), 400
    if not content or not isinstance(content, str):
        return jsonify({"message":"Must have valid content"}), 400
    if category is not None and not isinstance(category, str):
        return jsonify({"message":"Category must be a string"}), 400
    if not isinstance(tags, list):
        return jsonify({"message":"tag must be a list"}), 400
    
    # ensure all tags are strings
    cleaned_tags = []
    for t in tags:
        if isinstance(t, str):
            cleaned_tags.append(normalize_tag(t))
    tags = cleaned_tags

    # ensure tables exist
    create_table()

    conn = get_db()
    c = conn.cursor()

    # Insert blog
    c.execute("""
        INSERT INTO blogs (title, content, category)
        VALUES (?, ?, ?)
    """, (title, content, category))

    blog_id = c.lastrowid  # get ID of the inserted blog

    # Insert tags one by one, link to blog
    for tag in tags:
        # insert tag if not exist
        c.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
        
        # retrieve tag_id (whether newly created or existing)
        c.execute("SELECT id FROM tags WHERE name = ?", (tag,))
        tag_id = c.fetchone()["id"]

        # link blog + tag
        c.execute("""
            INSERT OR IGNORE INTO blog_tags (blog_id, tag_id)
            VALUES (?, ?)
        """, (blog_id, tag_id))

    conn.commit()

    # Select creation and update time from blogs
    c.execute("""
              SELECT createdAt, updatedAt FROM blogs
              WHERE id = ?  
          """, (blog_id,))
    row = c.fetchone()
    createdAt = row["createdAt"]
    updatedAt = row["updatedAt"]
    conn.close()

    return jsonify({
        "message": "Blog created successfully!", 
        "id": blog_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "createdAt": createdAt,
        "updatedAt": updatedAt
    }), 201

# update route
@app.route("/api/blog/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message":"Bad request"}), 400
    
    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    tags = data.get("tags", [])  # list of strings

    # validate data
    if not title or not isinstance(title, str):
        return jsonify({"message":"Must have title"}), 400
    
    if not content or not isinstance(content, str):
        return jsonify({"message":"Must have content"}), 400
    
    if category is not None and not isinstance(category, str):
        return jsonify({"message":"Category must be a string"}), 400
    
    if not isinstance(tags, list):
        return jsonify({"message":"tags must be a list"}), 400
    
    #normalise tags
    tags = [normalize_tag(t) for t in tags[:10]]

    if len(title) > 200:
        return jsonify({"message":"title too long"}), 400
    
    if len(content) > 10000:
        return jsonify({"message":"content too long"}), 400
    
    # Update data in table
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        UPDATE blogs 
        SET title = ?, content = ?, category = ?, updatedAt = DATE('now')
        WHERE id = ?
        """, (title, content, category, id))
    if c.rowcount == 0:
        conn.close()
        return jsonify({"message":"Blog not found"}), 404
    
    conn.commit()

    c.execute("""
            SELECT createdAt, updatedAt FROM blogs
            WHERE id = ?
         """, (id,))
    row = c.fetchone()
    createdAt = row["createdAt"]
    updatedAt = row["updatedAt"]

    return jsonify({
        "id": id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "createdAt": createdAt,
        "updatedAt": updatedAt
    }), 200
    

# delete route
@app.route("/api/blog/<delete>")
def delete(delete):
    ...



