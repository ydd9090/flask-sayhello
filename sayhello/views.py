
from flask import flash,redirect,url_for,render_template,request,send_from_directory,session
from flask_login import login_required,login_user,logout_user,current_user

from sayhello import app,db
from sayhello.models import Message,User
from sayhello.forms import HelloForm,LoginForm,RegisterForm
from sayhello.utils import redirect_back

@app.route("/",methods=["GET","POST"])
def index():
    page = request.args.get("page",1,type=int)
    message_count = Message.query.count()
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page=page,per_page=10)
    messages = pagination.items
    form = HelloForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("请登录后再操作")
            return redirect(url_for("login"))
        name = form.name.data
        body = form.body.data
        message = Message(name = name,body = body,user = current_user._get_current_object())
        db.session.add(message)
        db.session.commit()
        flash("Your message hava been sent to the world!")
        session["message_name"] = name
        return redirect(url_for("index"))
    form.name.data = session.get("message_name") or current_user._get_current_object().username  # 需要通过session or 上下文变量传递给redirect后的请求
    return render_template("index.html",form=form,messages=messages,pagination=pagination,message_count=message_count)

@app.route("/about")
@login_required
def about():
    user = current_user._get_current_object()
    return render_template("about.html",user=user)

@app.route("/avatars/<path:filename>")
def get_avatar(filename):
    return send_from_directory(app.config["AVATARS_SAVE_PATH"],filename)

@app.route("/list/<int:user_id>")
def list(user_id):

    page = request.args.get("page",1,type=int)
    pagination = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp.desc()).paginate(page=page,per_page=5)
    message_count = Message.query.filter_by(user_id=user_id).count()
    messages = pagination.items

    return render_template("list.html",messages=messages,pagination=pagination,message_count=message_count)

@app.route("/top/<int:message_id>",methods=["POST"])
@login_required
def set_top(message_id):
    message = Message.query.get_or_404(message_id)
    message.set_top()
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user,form.remember.data)
            flash("登录成功")
            # return redirect_back()
            return redirect(url_for("index"))
        flash("用户名或密码错误🙅")
    return render_template("login.html",form=form)

@app.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("您已退出登录")
    return redirect(url_for("index"))


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        description = form.description.data
        user = User(username=username,description=description)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for("login"))
    return render_template("register.html",form=form)

    
    
    




    

