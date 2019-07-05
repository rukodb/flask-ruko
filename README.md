# Flask Ruko

*Ruko integration for Flask*

Flask-Ruko is a simple [Flask](http://flask.pocoo.org/) integration for [ruko](https://github.com/rukodb/ruko-python) server.

## Installation

```bash
pip install flask-ruko
```

## Usage

```python
from flask import Flask
from flask_ruko import RukoDB

app = Flask(__name__)
db = RukoDB(app, '0.0.0.0', 44544)

users = db['users']  # db is an instance of RDict

@app.route('/users/<uuid>', methods=['GET'])
def get_user(uuid):
    return users.by('uuid')[uuid]()

```
