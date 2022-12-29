import os

from sayhello import app

dev_db= "sqlite:///" + os.path.join(os.path.dirname(app.root_path),"data.db")

SECRET_KEY = os.getenv("SECRET_KEY","secret_strings")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI",dev_db)



if __name__ == "__main__":
    print(dev_db)