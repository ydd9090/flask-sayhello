from sayhello import app,db
from sayhello.models import Message,User
import click


@app.cli.command()
@click.option("--drop",is_flag=True,help="Create after drop.")
def initdb(drop):
    '''initialize database'''
    if drop:
        click.confirm('This operation will delete the database,do you want to continue?',abort=True)
        db.drop_all()
    db.create_all()
    user = User(username="admin")
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
    click.echo("Initialize database.")


@app.cli.command()
@click.option("--count",default=20,help="Quantity of messages,default is 20.")
def forge(count):
    """Generate fake messages."""
    from faker import Faker
    # db.drop_all()
    db.create_all()

    faker = Faker("zh_CN")
    click.echo("Working...")
    user = User.query.first()
    for i in range(count):
        message = Message(name=faker.name(),body = faker.sentence(),timestamp=faker.date_time_this_year(),user=user)
        db.session.add(message)
    db.session.commit()
    click.echo(f"Created {count} fake messages.")


@app.cli.command()
@click.option("--count",default=20,help="num of numbers.")
def test_num(count):
    nums = [0,1,2,3,4,5,6,7,8,9]
    import random
    for _ in range(count):
        print(random.choice(nums),end="")
    click.echo("\ndone.")


