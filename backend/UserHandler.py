import abc
import util
import const

class UserHandler:
    @abc.abstractmethod
    def onNewUser(self, user_id):
        raise NotImplementedError()
        
    @abc.abstractmethod
    def onUserLogin(self, user_id):
        raise NotImplementedError()

class UserHandlerImpl(UserHandler):
	def onNewUser(self, user_model, coupon_model, user_id):
		# send email to new user
		user = user_model.getUserById(user_id)
		if user:
			util.sendEmail([user.email], util.getWelcomEmailContent(user.username))

		# add coupon
		coupon_id = const.NEW_USER_COUPON_ID
		coupon_model.addCoupon(user_id, coupon_id, 1)

	def onUserLogin(self, user_id):
		pass
