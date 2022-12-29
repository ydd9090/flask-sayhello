from sayhello import app,db
from sayhello.models import Message
import click


@app.cli.command()
@click.option("--drop",is_flag=True,help="Create after drop.")
def initdb(drop):
    '''initialize database'''
    if drop:
        click.confirm('This operation will delete the database,do you want to continue?',abort=True)
        db.drop_all()
    db.create_all()
    click.echo("Initialize database.")


@app.cli.command()
@click.option("--count",default=20,help="Quantity of messages,default is 20.")
def forge(count):
    """Generate fake messages."""
    from faker import Faker
    db.drop_all()
    db.create_all()

    faker = Faker()
    click.echo("Working...")
    for i in range(count):
        message = Message(name=faker.name(),body = faker.sentence(),timestamp=faker.date_time_this_year())
        db.session.add(message)
    db.session.commit()
    click.echo(f"Created {count} fake message.")


