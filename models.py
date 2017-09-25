from app import db
import re

class BlogPost(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    date = db.Column(db.String)
    post_link = db.Column(db.String)

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date
        lowercase = re.compile(r' ')
        self.post_link = lowercase.sub('_', title).lower()
    
    def __repr__(self):
        return f"{self.title} ||| {self.text[:20]}"
