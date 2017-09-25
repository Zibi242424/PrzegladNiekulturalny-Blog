from app import db
from models import BlogPost
from datetime import datetime
from pytz import timezone

poland = timezone('Europe/Warsaw')
date = str(datetime.now(poland))[:-13] 

db.create_all()

db.session.add(BlogPost("Hi Zuzia!", "This is the first post", date))

db.session.commit()