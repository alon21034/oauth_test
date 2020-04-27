import const
import abc

class Coupon:
	__id: int
	__user_id: str
	__count: int

	def __init__(self, id, user_id, count):
		self.__id = id
		self.__user_id = user_id
		self.__count = count

	@property
	def id(self):
		return self.__id

	@property
	def user_id(self):
		return self.__user_id

	@property
	def count(self):
		return self.__count

class CouponModel:

	@abc.abstractmethod
	def addCoupon(self, user_id, coupon_id, count = 1):
		raise NotImplementedError()

	@abc.abstractmethod
	def getCouponCount(self, user_id, coupon_id):
		raise NotImplementedError()

	@abc.abstractmethod
	def getAllCoupon(self, user_id):
		raise NotImplementedError()

class CouponModelImpl(CouponModel):

	def __init__(self, db):
		self._db = db

	def addCoupon(self, user_id, coupon_id, count = 1):
		coupon_count = self.getCouponCount(user_id, coupon_id)
		if coupon_count:
			# update coupon number
			c = self._db.cursor()
			c.execute("UPDATE coupon SET '{}'={} WHERE {}={} AND {}={}"
				.format(const.COUPON_COUNT, coupon_count+coupon, const.COUPON_USER_ID, user_id, const.COUPON_COUPON_ID, coupon_id))
			self._db.commit()
			return coupon_count + count
		else:
			# create coupon record
			c = self._db.cursor()
			coupon_id = c.execute("INSERT INTO coupon ('{}', '{}', '{}') values ('{}', '{}', '{}')"
				.format(const.COUPON_USER_ID, const.COUPON_COUPON_ID, const.COUPON_COUNT, user_id, coupon_id, count))
			self._db.commit()
			return coupon_id

	def getCouponCount(self, user_id, coupon_id):
		c = self._db.cursor()
		coupon_info = c.execute("SELECT count FROM coupon WHERE {}={} AND {}={}"
			.format(const.COUPON_USER_ID, user_id, const.COUPON_COUPON_ID, coupon_id))
		rows = c.fetchall()
		if len(rows) == 0:
			return False
		else :
			return rows[0][0]

	def getAllCoupon(self, user_id):
		c = self._db.cursor()
		coupon_info = c.execute("SELECT * FROM coupon WHERE {}={}".
			format(const.COUPON_USER_ID, user_id))
		rows = c.fetchall()
		return rows

