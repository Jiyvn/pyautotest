

class Descriptor(object):

    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)
        if 'default' in opts:
            self.__dict__.update({self.name: opts.get('default')})

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class TypedMeta(type):

    def __new__(cls, clsname, bases, methods):
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


class Typed(Descriptor):
    """Values must of a particular type"""

    expected_type = type(None)
    allow_none = False

    def __init__(self, *args, **kw):
        super(Typed, self).__init__(*args, **kw)
        self.__doc__ = "Values must be of type {0}".format(self.expected_type)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            if not self.allow_none or (self.allow_none and value is not None):
                raise TypeError('expected ' + str(self.expected_type))
        super(Typed, self).__set__(instance, value)

    # def __repr__(self):
    #     return self.__doc__


def DecrTyped(expected_type, cls=None):
    if cls is None:
        return lambda cls: DecrTyped(expected_type, cls)
    super_set = cls.__set__  # keep __set__() of cls

    if 'allow_none' not in cls.__dict__:
        allow_none = False
    else:
        allow_none = cls.allow_none

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            if not allow_none or (allow_none and value is not None):
                raise TypeError('expected ' + str(self.expected_type))
        super_set(self, instance, value)

    cls.__set__ = __set__  # customize current cls.__set__()
    return cls


@DecrTyped(int)
class Integer(Descriptor):
    pass


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


@DecrTyped(bool)
class Boolean(Descriptor):
    expected_type = bool


class IntFloat(Typed):
    expected_type = (int, float)


class Dict(Typed, dict):
    expected_type = dict

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class List(Typed):
    expected_type = list

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Tuple(Typed, tuple):
    expected_type = tuple

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Union(Typed, list):
    expected_type = (list, tuple)

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
