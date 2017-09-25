from app import db
from models import BlogPost

db.create_all()

db.session.add(BlogPost("im good", "well", "asd"))

db.session.commit()