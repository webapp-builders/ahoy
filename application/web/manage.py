from flask.ext.script import Command, Manager, Option, Server,prompt_bool
from app.models.user import User,load_user
from app.config.extensions import db
from app import create_app
import uuid

app = create_app()
manager = Manager(app)

############
#python manage.py hello
@manager.command
def hello():
    print "hello"

#python manage.py hello -n areg
@manager.option('-n')
def hello(name):
    print "hello ", name

@manager.option('-a', '--name', dest='name', default='areg')
@manager.option('-u', '--url', dest='url', default=None)
def hello(name, url):
    print name + " " + url

############

 #\l #list databases
#\d #list tables
#\d tablename #list table columns
#\q #quit
#python manage.py initdb
@manager.command
def initdb():
    db.create_all()
    print "initialized database"



#python manage.py dropdb
@manager.command
def dropdb():
    if prompt_bool("are you sure?"):
        db.drop_all()
        print "dropped database"

#python manage.py adduser
@manager.command
def adduser():
    user = User(username="arega",
                email="arega@gmail.com",
                password="panama",
                signin_token=uuid.uuid4().hex)
    user = User(username="aregb",
                email="aregb@gmail.com",
                password="panama",
                signin_token=uuid.uuid4().hex)
    db.session.add(user)
    db.session.commit()


#python manage.py runserver
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

print app.config
print app.url_map


if __name__ == '__main__':
    #help command
    #python manage.py runserver -?
    manager.run()
