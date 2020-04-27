import hashlib
import abc
import time
import const
from util import *

class Token:
    __id: int
    __user_id: int
    __token: str

    def __init__(self, id, user_id, token):
        self.__id = id
        self.__user_id = user_id
        self.__token = token

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def token(self):
        return self.__token

class TokenModel:
    @abc.abstractmethod
    def createToken(self, user_id):
        raise NotImplementedError()

class TokenModelImpl(TokenModel):
    def __init__(self, db):
        self._db = db

    def createToken(self, user_id):
        c = self._db.cursor()
        token = generateToken()
        c.execute("INSERT INTO token ('{}', '{}') VALUES ('{}', '{}')"
            .format(const.TOKEN_USER_ID, const.TOKEN_TOKEN, user_id, token))
        self._db.commit()
        return token

    def getUser(self, token):
        c = self._db.cursor()
        c.execute("SELECT {} FROM token WHERE {}='{}'".
            format(const.TOKEN_USER_ID, const.TOKEN_TOKEN, token))
        rows = c.fetchone()
        if not rows:
            return False
        return rows[0]