from sayhello import db
from datetime import datetime
from flask_avatars import Identicon

class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(200),)
    name = db.Column(db.String(20),index=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))


    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        self.generate_avatar()


    def generate_avatar(self,):
        avatar = Identicon()
        filenames = avatar.generate(text=self.name.replace(" ","_"))
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]