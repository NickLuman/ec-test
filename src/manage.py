import os 

from flask.cli import FlaskGroup

from converter.app import app

# os.environ["FLASK_APP"] = "src/converter/app.py"

cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()