## Installation

1. Clone this repository
```
$ git clone https://github.com/SyrymAbdikhan/Carbon-Footprint-Calculator
$ cd Carbon-Footprint-Calculator
```

2. Create a virtual environment and activate it
```
$ python -m venv venv
$ source ./venv/bin/activate
```

3. Install the dependencies
```
$ pip install -r requirements.txt
```

4. Create the tables
```
$ export FLASK_APP=./src/app
$ flask shell
```
```
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. Run the application
```
$ python ./src/app.py
```

6. To see the application, open this url in browser
```
http://127.0.0.1:8888/
```
