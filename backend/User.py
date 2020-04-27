import abc
from RegisterException import *
import const
from email_validator import validate_email, EmailNotValidError

class User:
    __id: int
    __username: str
    __password: str
    __email: str

    def __init__(self, username, password, email):
        self.__username = username
        self.__password = password
        self.__email = email
        
        # check data is valid
        self.checkEmptyUsername(self.__username)
        self.checkPasswordFormat(self.__password)
        self.checkEmailValid(self.__email)

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def email(self):
        return self.__email

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    def checkEmptyUsername(self, username):
        if len(username) == 0:
            raise WronUsernameFormatException()

    def checkEmailValid(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            raise WrongEmailFormatException();

    def checkPasswordFormat(self, password):
        if len(password) < 8:
            raise PasswordFormatException();

class UserModel:
    @abc.abstractmethod
    def createUser(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def login(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getUserById(self):
        raise NotImplementedError()

class UserModelImpl(UserModel):

    def __init__(self, db):
        self._db = db

    def createUser(self, user: User) -> int:
        c = self._db.cursor()

        # check username duplicate
        c.execute("SELECT * FROM user WHERE {}='{}'"
            .format(const.USER_NAME, user.username))
        rows = c.fetchall()
        if (len(rows) > 0):
            raise DuplicatedUsernameException()

        # check email duplicate
        c.execute("SELECT * FROM user WHERE {}='{}'"
            .format(const.USER_EMAIL, user.email))
        rows = c.fetchall()
        if (len(rows) > 0):
            raise DuplicatedEmailException()

        # create user
        c.execute("INSERT INTO user ('{}', '{}', '{}') VALUES ('{}', '{}', '{}')"
            .format(const.USER_NAME, const.USER_PASSWORD, const.USER_EMAIL, user.username, user.password, user.email))
        self._db.commit()

        return c.lastrowid

    def login(self, username, password):
        print(username, password)
        # if success, return token; else return False
        c = self._db.cursor()
        c.execute("SELECT * FROM user WHERE {}='{}' AND {}='{}'"
            .format(const.USER_NAME, username, const.USER_PASSWORD, password))
        rows = c.fetchall()

        if len(rows) == 1:
            user_id = rows[0][0]
            return user_id
        else:
            return False

    def getUserById(self, user_id):
        c = self._db.cursor()
        c.execute("SELECT * FROM user WHERE {}='{}'"
            .format(const.USER_ID, user_id))
        rows = c.fetchall()

        if len(rows) == 1:
            user = User(rows[0][1], rows[0][2], rows[0][3])
            user.id = rows[0]
            return user
        else: 
            return False
