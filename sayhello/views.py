
from flask import flash,redirect,url_for,render_template,request,send_from_directory
from sayhello import app,db
from sayhello.models import Message
from sayhello.forms import HelloForm

@app.route("/",methods=["GET","POST"])
def index():
    page = request.args.get("page",1,type=int)
    message_count = Message.query.count()
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page=page,per_page=10)
    messages = pagination.items
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name,body=body)
        db.session.add(message)
        db.session.commit()
        flash("Your message hava been sent to the world!")
        return redirect(url_for("index"))
    return render_template("index.html",form=form,messages=messages,pagination=pagination,message_count=message_count)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/avatars/<path:filename>")
def get_avatar(filename):
    return send_from_directory(app.config["AVATARS_SAVE_PATH"],filename)


@app.route("/list/<string:name>")
def list(name):
    page = request.args.get("page",1,type=int)
    pagination = Message.query.filter_by(name=name).order_by(Message.timestamp.desc()).paginate(page=page,per_page=5)
    message_count = Message.query.filter_by(name=name).count()
    messages = pagination.items

    return render_template("list.html",messages=messages,pagination=pagination,message_count=message_count)



    

