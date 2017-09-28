from app import db
from models import BlogPost
from datetime import datetime
from pytz import timezone

poland = timezone('Europe/Warsaw')
date = str(datetime.now(poland))[:-13] 

db.create_all()

db.session.add(BlogPost("Kat. film1", "jakis header", "post 1", date, "Film"))
db.session.add(BlogPost("Kat. film2", "inny header", "post 2", date, "Muzyka"))
db.session.add(BlogPost("Kat. film3", "jeszce inny", "post 2", date, "Film"))
db.session.add(BlogPost("Kat. film4", "header be sensu", "post 3", date, "Film"))

db.session.commit()