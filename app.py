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
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    tags = data.get("tags", [])  # list of strings
    tags = [normalize_tag(t) for t in tags]

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
    conn.close()

    return jsonify({"message": "Blog created successfully!", "blog_id": blog_id})

# update route
@app.route("/api/blog/<update>", methods=["GET"])
def update(update):
    ...

# delete route
@app.route("/api/blog/<delete>")
def delete(delete):
    ...



