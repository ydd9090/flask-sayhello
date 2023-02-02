import os

from sayhello import app

dev_db= "sqlite:///" + os.path.join(os.path.dirname(app.root_path),"data.db")

SECRET_KEY = os.getenv("SECRET_KEY","secret_strings")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI",dev_db)
AVATARS_SAVE_PATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),"uploads"),"avatars")

DEBUG_TB_INTERCEPT_REDIRECTS  = False # DEBUG_TB_INTERCEPT_REDIRECTS  = os.getenv("DEBUG_TB_INTERCEPT_REDIRECTS") or False
 



if __name__ == "__main__":
    print(AVATARS_SAVE_PATH)