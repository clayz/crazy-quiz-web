from protorpc import messages

DEFAULT_GEM = 5
DEFAULT_COIN = 100


class UserStatus(messages.Enum):
    ACTIVE = 1
    INACTIVE = 2
    WITHDRAWAL = 9


class Gender(messages.Enum):
    MALE = 1
    FEMALE = 2


class AccountType(messages.Enum):
    FACEBOOK = 1
    TWITTER = 2
    INSTAGRAM = 3


class Device(messages.Enum):
    IPHONE = 1
    IPAD = 2
    ANDROID = 3


class APIStatus(messages.Enum):
    SUCCESS = 100000
    ERROR = 999999

    # authorization and authentication
    ACCESS_DENY = 100001
    PERMISSION_DENY = 100002
    TOKEN_INVALID = 100003

    # API related
    API_NOT_FOUND = 101001
    PARAMETER_ERROR = 101002

    # data related
    DATA_NOT_FOUND = 102001
    DATA_SAVE_FAILED = 102002