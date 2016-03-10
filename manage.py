from flask.ext.script import Manager
from app import create_app

manager = Manager(create_app(), with_default_commands=True)

if __name__ == "__main__":
    manager.run()