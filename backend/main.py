import flask
import const
import util
import json
import sqlite3
from flask import request, abort
from flask_cors import cross_origin
from RegisterException import *
from User import User, UserModel, UserModelImpl
from UserHandler import UserHandlerImpl
from Coupon import CouponModelImpl
from Token import TokenModelImpl
from OauthHandler import OauthFactory, OauthHandler, OauthException
from db import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True
DATABASE = './{}'.format(const.DB_NAME)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    # get arguments
    username = request.form[const.KEY_NAME]
    password = request.form[const.KEY_PASSWORD]
    res = _login(username, password)
    return res if res else "{}".format({const.KEY_RESULT: False})

@app.route('/oauth', methods=['POST'])
@cross_origin()
def oauth_signup():
    # get argumants
    provider = request.form[const.KEY_PROVIDER]
    token = request.form[const.KEY_TOKEN]

    # register
    try:
        oauth_handler = OauthFactory.getHandler(provider, token)
        user = oauth_handler.createUser()
        _createUser(user)
        res = _login(user.username, user.password)
        return res if res else json.dumps({const.KEY_RESULT:False})
    except OauthException as e:
        return json.dumps({const.KEY_ERROR: str(e)})
    except (DuplicatedUsernameException, DuplicatedEmailException) as e:
        # already registered
        res = _login(oauth_handler.username, oauth_handler.password)
        return res if res else json.dumps({const.KEY_RESULT:False, const.KEY_MESSAGE:str(e)})
    except Exception as e:
        print(e)
        return json.dumps({const.KEY_RESULT:False})

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    # get argements
    username = request.form[const.KEY_NAME]
    password = request.form[const.KEY_PASSWORD]
    email = request.form[const.KEY_EMAIL]

    try:
        user = User(username, password, email)
        _createUser(user)
    except RegisterException as e:
        # handle error
        return json.dumps({const.KEY_RESULT:False, const.KEY_MESSAGE:str(e)})

    return json.dumps({const.KEY_RESULT: True})

@app.route('/coupon', methods=['GET'])
@cross_origin()
def getCoupon():
    token = request.args[const.KEY_TOKEN]
    db = get_db()
    token_model = TokenModelImpl(db)
    user_id = token_model.getUser(token)
    if not user_id:
        abort(401)
    coupon_model = CouponModelImpl(db)
    coupons = coupon_model.getAllCoupon(user_id)
    return str(coupons)

### Business Login ###

def _login(username, password):
    db = get_db()
    user_model = UserModelImpl(db)
    user_id = user_model.login(username, password)

    if user_id:
        # login success, generate token.
        token_model = TokenModelImpl(db)
        token = token_model.createToken(user_id)
        return "{}".format({const.KEY_TOKEN: token})
    else:
        # login fail
        return False

def _createUser(user):
    db = get_db()
    user_model = UserModelImpl(db)
    user_id = user_model.createUser(user)
    
    # new user created event
    coupon_model = CouponModelImpl(db)

    user_handler = UserHandlerImpl()
    user_handler.onNewUser(user_model, coupon_model, user_id)

if __name__ == "__main__":
    app.run()