from flask import url_for
from flask_login import LoginManager,AnonymousUserMixin
from flask_wtf import CSRFProtect


login_manager = LoginManager()
login_manager.login_view = "login"

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from sayhello.models import User
    user = User.query.get(int(user_id))
    return user


class Guest(AnonymousUserMixin):
    username = None

    def can(self,permission_name):
        return False
    
    @property
    def is_admin(self,):
        return False
    
login_manager.anonymous_user = Guest
    
