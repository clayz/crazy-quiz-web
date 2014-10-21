from protorpc import messages


class UserStatus(messages.Enum):
    ACTIVE = 1
    INACTIVE = 2
    WITHDRAWAL = 3


class Gender(messages.Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class AccountType(messages.Enum):
    FACEBOOK = 1
    TWITTER = 2
    INSTAGRAM = 3


class Device(messages.Enum):
    UNKNOWN = 0
    IPHONE = 1
    IPAD = 2
    ANDROID = 3