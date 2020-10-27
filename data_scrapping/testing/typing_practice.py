from typing import List, Dict, Tuple, NewType, Sized, Union, Any
from typing import Iterable, Callable, Mapping, Sequence, TypeVar, Generic
from logging import Logger, getLogger, StreamHandler

print('----------Any--------------')

def hash_b(item: Any) -> int:
    pass

def hash_a(item: object) -> int:
    pass

def legacy_parser(text):
    pass

# A static type checker will treat the above
# as having the same signature as:
def legacy_parser(text: Any) -> Any:
    pass


a = None    # type: Any
a = []      # OK
a = 2       # OK

s = ''      # type: str
s = a       # OK

def foo(item: Any) -> int:
    return item

print(foo(None))
print(foo(2))

print('---------Generic-------------')
T = TypeVar('T', int, float, complex)
Vec = Iterable[Tuple[T,T]]

def inproduct(v: Vec[T]) -> T:
    return sum(x*y for x, y in v)

S = TypeVar('S')
Response = Union[Iterable[S], int]

def response(query: str) -> Response[str]:
    return [query, 1]

print(response('select is_follower from users;'))

T, Y = TypeVar('T'), TypeVar('Y')

class MyIterable(Iterable):
    pass
#     def __init__(self, name: Iterable[str], age: Iterable[int]) -> None:
#       self.name = name
#       self.age = age

#     def display_info(self) -> None:
#         print('{0} has {1} age'.format(self.name, self.age))


# _iterable = MyIterable('data', 1)
# _iterable.display_info()

class LinkedList(Sized, Generic[T]):
    pass

class Pair(Generic[T, Y]):
    pass

print('----------List, Dict, Tuple-------------')

Vector = List[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

# typechecks; a list of floats qualifies as a Vector.
new_vector = scale(2.0, [1.0, -4.2, 5.4])
print(new_vector)

ConnectionOption = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[ConnectionOption, Address]

def broadcast_message(message: str, server: List[Server]) -> None:
    print(message)

_connectionOption = ['dict1', 'dict2']
_address = ('tuple', 1)
_server = (_connectionOption, _address)

broadcast_message('test', _server)

UserId = NewType('UserId', 12)
some_id = UserId(524313)

def get_user_name(user_id : UserId) -> str:
    print(user_id)

get_user_name(some_id)

user_a = get_user_name(UserId(42351))

user_b = get_user_name(-1)

output = UserId(23413) + UserId(54341)

get_user_name(output)

print('---------AdminUser---------------')

class AdminUserId(int):
    pass

userId = NewType('UserId', int)

memberid = userId(1233)

print(memberid)

print(userId)

# class AdminUserId(userId):
#     pass

followerId = NewType('FollowerId', userId)
_followerId = followerId(123)
print(_followerId)

connectionOption = NewType('connection_str', List[str])
print(connectionOption(['local', '12.0.0.1']))

connectionOption = NewType('connection_str', Dict[str, str])
print(connectionOption({'ip':'127.0.0.1', 'user_name':'twitter'}))

print('---------Callable------------')

def get_next_item(_item: int) -> str:
    print('next account login id:',_item)
    return 'done'

def feeder(get_next_item: Callable[[int], str])->None:
    print(get_next_item)

feeder(get_next_item(12))

print('------------Mapping, Sequence---------------')

Employee = int

def notify_by_email(employees: Sequence[Employee], overrides: Mapping[str, str]) -> None:
    for employee, idx in enumerate(employees):
        print('employees {0}: {1}'.format(idx, employee))

    for key in overrides.keys():
        print('value in key {0} is {1}'.format(key, overrides[key]))

notify_by_email([1,2,3], {'id': 1})

print('----------Sequence, TypeVar--------------')

T = TypeVar('T')

def first(l: Sequence[T]) -> T:
    for item in l:
        print(item)

first([1, '1'])


print('--------LoggedVar-------------')

T = TypeVar('T', str, bool)

class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value
    
    def log(self, message: str) -> None:
        self.logger.info('%s: %s', self.name, message)

_logger = Logger(name='tweet_extract_log')
_logger.setLevel(level='INFO')
handler = StreamHandler()
handler.setLevel('INFO')
_logger.addHandler(handler)
_log = LoggedVar('tweet_extract', 'Data topic', _logger)
_log.log('starting log tweet_extract')

print('-------------Iterable---------------')

def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
    for var in vars:
        var.set('id')
        print(var.get())
logUser = LoggedVar(1, 'get all member in Data list', _logger)
logMember = LoggedVar[str](20, 'get all members', _logger)
zero_all_vars([logUser, _log, logMember])

print(LoggedVar[int])

