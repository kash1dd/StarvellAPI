class MyProfileProperty:
    def __init__(
        self,
        username,
        id,
        email,
        created_date,
        avatar_id,
        banner_id,
        description,
        is_verified,
        rating,
        review_count,
        balance_hold,
        balance,
        active_orders,
    ):
        self.__username = username
        self.__id = id
        self.__email = email
        self.__created_date = created_date
        self.__avatar_id = avatar_id
        self.__banner_id = (banner_id,)
        self.__description = description
        self.__is_verified = is_verified
        self.__rating = rating
        self.__reviews_count = review_count
        self.__balance_hold = balance_hold
        self.__balance = balance
        self.__active_orders = active_orders

    @property
    def username(self):
        return self.__username

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    @property
    def created_date(self):
        return self.__created_date

    @property
    def avatar_id(self):
        return self.__avatar_id

    @property
    def banner_id(self):
        return self.__banner_id

    @property
    def description(self):
        return self.__description

    @property
    def is_verified(self):
        return self.__is_verified

    @property
    def rating(self):
        return self.__rating

    @property
    def reviews_count(self):
        return self.__reviews_count

    @property
    def balance_hold(self):
        return self.__balance_hold

    @property
    def balance(self):
        return self.__balance

    @property
    def active_orders(self):
        return self.__active_orders
