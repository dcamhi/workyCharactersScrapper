# THIS FILE CREATES THE FLASK APP AND START SERVER

import os
from flask_script import Manager, Server
from flask_ci import CICommand

from application import create_app
import settings
import config

debug = config.DEBUG
host = os.getenv('IP', '0.0.0.0')
port = int(os.getenv('PORT', 8080))

app = create_app(debug)
manager = Manager(app)

manager.add_command("ci", CICommand(settings))
manager.add_command("runserver", Server(
    use_debugger=debug,
    use_reloader=debug,
    host=host,
    port=port
))


if __name__ == "__main__":
    manager.run()
