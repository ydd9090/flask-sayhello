from sayhello import db
from datetime import datetime
from flask_avatars import Identicon
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

roles_permissions = db.Table("roles_permissions",
                                db.Column("role_id",db.Integer,db.ForeignKey('role.id')),
                                db.Column("permission_id",db.Integer,db.ForeignKey('permission.id')))

class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(200),)
    name = db.Column(db.String(20),index=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    is_setted_top = db.Column(db.Boolean,default=False)
    set_top_timestamp = db.Column(db.DateTime,index=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    user = db.relationship("User",back_populates="messages")
    hiding = db.Column(db.Boolean,default=False)
    star_num = db.Column(db.Integer,default=0)

    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        self.generate_avatar()

    def generate_avatar(self,):
        avatar = Identicon()
        filenames = avatar.generate(text=self.name.replace(" ","_"))
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]

    def set_top(self,):
        self.is_setted_top = True
        self.set_top_timestamp = datetime.utcnow()
        db.session.commit()

    def star_it(self,):
        self.star = self.star + 1


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_pash = db.Column(db.String(128))
    messages = db.relationship("Message",back_populates="user")
    description = db.Column(db.String(1000))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    role = db.relationship("Role",back_populates="users")

    def set_password(self,password):
        self.password_pash = generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_pash,password)
    
    @property
    def is_admin(self):
        return self.role.name == "Administrator"
    
    def set_role(self,role_name = None):
        if self.role is None:
            role_name = role_name or "User"
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                raise Exception("set role error:{} role is not exist.".format(role_name))
            self.role = role
        db.session.commit()
    

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    permissions = db.relationship("Permission",secondary=roles_permissions,back_populates="roles")
    users = db.relationship("User",back_populates="role")

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['EXPLORE','STAR'],
            'User': ['EXPLORE','STAR', 'COMMENT'],
            'Administrator': ['EXPLORE','STAR', 'COMMENT', 'ADMINISTER']
        }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


class Permission(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    roles = db.relationship("Role",secondary=roles_permissions,back_populates="permissions")


