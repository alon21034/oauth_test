# Readme

## Build

### Environment

- Python 3.7.0
- Node v12.5.0

### Create SQLite Database
```
# init database
sudo apt-get install sqlite3
cd ./backend
sqlite3 -init schema.sql test.db
```

### Run Flask App for Backend
```
cd ./backend/
# python venv
virtualenv -p python3 env
source ./env/bin/activate

# install dependencies
pip3 install -r requirement

# start backend server
python3 main.py

# The Backend server will run at localhost:5000
```

### Run React App for Frontend
```
cd ./frontend
npm install --save
npm start

# The frontend app will run at localhost:3000
```

## API

### POST /register

> Note that the password should be pass to backend server after `hash`, but for demo purpose, I skip this step for now.

#### params: 
- username
- password
- email

### POST /login

#### params:
- username
- password

### POST /oauth

#### params:
- provider: only support 'google' or 'facebook' now.
- token

### GET /coupon

#### params:
- token

