import const

class RegisterException(Exception):
    pass

class WronUsernameFormatException(RegisterException):
	def __str__(sefl):
		return const.USERNAME_FORMAT_ERROR

class WrongEmailFormatException(RegisterException):
    def __str__(self):
        return const.EMAIL_FORMAT_ERROR

class DuplicatedEmailException(RegisterException):
    def __str__(self):
        return const.DUPLICATED_EMAIL_ERROR

class DuplicatedUsernameException(RegisterException):
    def __str__(self):
        return const.DUPLICATED_USERNAME_ERROR

class PasswordFormatException(RegisterException):
    def __str__(self):
        return const.PASSWORD_FORMAT_ERROR
