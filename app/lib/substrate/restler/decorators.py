
from restler import UnsupportedTypeError

def unsupported(type_):
    """
    Mark types for that aren't supported
    :param type_: Model type
    :return: a handler that raises and UnsupportedTypeError for that type
    """
    def handler(obj):
        raise UnsupportedTypeError(type_)
    return handler

def wrap_method(cls, method):
    """ Helper function to help wrap _restler* methods when more
     than on decorator is used on a model.
    :param method: method to wrap
    """
    from copy import copy
    method_name = method.__func__.__name__
    method_param = method
    if hasattr(cls, method_name):
        orig_cls_method = getattr(cls, method_name)

        @classmethod
        def wrap(cls_):
            setattr(cls, method_name, method_param)
            method = getattr(cls, method_name)
            aggregate = copy(orig_cls_method())
            if isinstance(aggregate, list):  # _restler_types()
                aggregate = set(aggregate)
                aggregate.update(method())
                aggregate = list(aggregate)
            elif isinstance(aggregate, dict):  # _restler_property_map
                aggregate.update(method())
            elif isinstance(aggregate, str):
                # Developer shouldn't really do this, but we'll try
                # to do the correct thing and use the most recently defined name
                aggregate = method()  # _restler_serialization_name
            return aggregate
        setattr(cls, method_name, wrap)
    else:
        setattr(cls, method_name, method)

def create_type_map(cls, type_map=None):
    """ Helper function for creating type maps """

    _type_map = None
    if type_map:
        if callable(type_map):
            _type_map = type_map(cls)
        else:
            _type_map = type_map.copy()
    else:
        _type_map = {}

    return _type_map

def create_serialization_name(cls, serialization_name=None):
    """ Helper function for creating a serialization name """

    _serialization_name = serialization_name
    if serialization_name:
        if callable(serialization_name):
            _serialization_name = serialization_name(cls)
    return _serialization_name

def create_property_map(cls, property_map=None):
    """ Helper function for creating property maps """

    _property_map = None
    if property_map:
        if callable(property_map):
            _property_map = property_map(cls)
        else:
            _property_map = property_map.copy()
    else:
        _property_map = {}
    return _property_map

def ae_db_decorator_builder(type_map=None, serialization_name=None, property_map=None):
    """
    Creates a decorator for google.appengine.ext.db.Model
    :param type_map: a map of types -> callable(value) or a callable(model)
     that returns a map.
    :param serialization_name: a (string) name used for the tag/key for serialization or
     a callable(model) that returns a name
    :param property_map: a map of (field) names (string) -> types or a callable(model)
     that returns a map.
    """
    from google.appengine.ext import blobstore, db

    def wrap(cls):
        """
        Restler serialization class decorator for google.appengine.ext.db.Model
        """

        @classmethod
        def _restler_types(cls):
            """
            A map of types types to callables that serialize those types.
            """

            _type_map = create_type_map(type_map)

            from google.appengine.api import users
            from webapp2 import cached_property
            _type_map.update(
                {
                    db.Query: lambda query: [obj for obj in query],
                    db.GeoPt: lambda obj: "%s %s" % (obj.lat, obj.lon),
                    db.IM: lambda obj: "%s %s" % (obj.protocol, obj.address),
                    users.User: lambda obj: obj.user_id() or obj.email(),
                    cached_property: lambda obj: cached_property,
                    blobstore.BlobInfo: lambda obj: str(obj.key())  # TODO is this correct?
            })
            return _type_map

        @classmethod
        def _restler_serialization_name(cls):
            """
            The lowercase model classname
            """
            _serialization_name = create_serialization_name(cls, serialization_name or cls.kind().lower())
            return _serialization_name

        @classmethod
        def _restler_property_map(cls):
            """
            List of model property names -> property types. The names are used in
            *include_all_fields=True* Property types must be from
            **google.appengine.ext.db.Property**
            """
            _property_map = create_property_map(cls, property_map)
            _property_map.update(cls.properties())
            return _property_map

        wrap_method(cls, _restler_types)
        wrap_method(cls, _restler_property_map)
        cls._restler_serialization_name = _restler_serialization_name

        return cls

    return wrap

ae_db_serializer = ae_db_decorator_builder()

def ae_ndb_decorator_builder(type_map=None, serialization_name=None, property_map=None):
    """
    Restler serializationclass decorator for google.appengine.ext.ndb.Model
    """
    from google.appengine.ext import ndb

    def wrap(cls):

        @classmethod
        def _restler_types(cls):
            """
            A map of types types to callables that serialize those types.
            """
            from google.appengine.api import users
            from webapp2 import cached_property
            _type_map = create_type_map(type_map)
            _type_map.update({
                ndb.query.Query: lambda query: [obj for obj in query],
                ndb.ComputedProperty: unsupported(ndb.ComputedProperty),
                ndb.GenericProperty: unsupported(ndb.GenericProperty),
                ndb.GeoPt: lambda obj: "%s %s" % (obj.lat, obj.lon),
                ndb.PickleProperty: unsupported(ndb.PickleProperty),
                users.User: lambda obj: obj.user_id() or obj.email(),
                cached_property: lambda obj: cached_property,
            })
            return _type_map

        @classmethod
        def _restler_serialization_name(cls):
            """
            The lowercase model classname
            """
            _serialization_name = create_serialization_name(cls, serialization_name or cls.__name__.lower())
            return _serialization_name

        @classmethod
        def _restler_property_map(cls):
            """
            List of model property names if *include_all_fields=True*
            Property must be from **google.appengine.ext.ndb.Property**
            """
            _property_map = create_property_map(cls, property_map)
            _property_map.update(dict((name, prop.__class__) for name, prop in cls._properties.items()))
            return _property_map

        wrap_method(cls, _restler_types)
        wrap_method(cls, _restler_property_map)
        cls._restler_serialization_name = _restler_serialization_name

        return cls
    return wrap

ae_ndb_serializer = ae_ndb_decorator_builder()

def django_decorator_builder(type_map=None, serialization_name=None, property_map=None):
    """
    Creates a decorator for django.db.Models
    :param type_map: a map of types -> callable(value) or a callable(model)
     that returns a map.
    :param serialization_name: a (string) name used for the tag/key for serialization or
     a callable(model) that returns a name
    :param property_map: a map of (field) names (string) -> types or a callable(model)
     that returns a map.
    """

    def wrap(cls):
        """
        Restler serialization class decorator for django.db.models
        """
        @classmethod
        def _restler_types(cls):
            """
            A map of types types to callables that serialize those types.
            """
            from django.db.models.query import QuerySet
            from django.db.models import CommaSeparatedIntegerField, FileField, FilePathField, ImageField
            import json
            _type_map = create_type_map(type_map)
            _type_map.update({
                QuerySet: lambda query: list(query),
                CommaSeparatedIntegerField: lambda value: json.loads(value),
                ImageField: unsupported(ImageField),
                FileField: unsupported(FileField),
                FilePathField: unsupported(FilePathField)
            })
            return _type_map

        @classmethod
        def _restler_serialization_name(cls):
            """
            The lowercase model classname
            """
            _serialization_name = create_serialization_name(cls, serialization_name or cls.__name__.lower())
            return _serialization_name

        @classmethod
        def _restler_property_map(cls):
            """
            List of model property names -> property types. The names are used in
            *include_all_fields=True* Property must be from **django.models.fields**
            """
            from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField, RelatedObject
            # Relation fields (and their related objects) need to be handled specifically as there is no single way to
            # handle them -- they should be handled explicity through callables.
            excluded_types = {ForeignKey, ManyToManyField, OneToOneField, RelatedObject}
            name_map = cls._meta._name_map
            all_field_names = cls._meta.get_all_field_names()
            _property_map = create_property_map(cls, property_map)
            new_property_map = dict([(name, name_map[name][0].__class__)
                             for name in all_field_names if name_map[name][0].__class__ not in excluded_types])
            _property_map.update(new_property_map)
            return _property_map

        wrap_method(cls, _restler_types)
        wrap_method(cls, _restler_property_map)
        cls._restler_serialization_name = _restler_serialization_name

        return cls
    return wrap

django_serializer = django_decorator_builder()


def sqlalchemy_decorator_builder(type_map=None, serialization_name=None, property_map=None):
    """
    Creates a decorator for sqlalchemy models
    :param type_map: a map of types -> callable(value) or a callable(model)
     that returns a map.
    :param serialization_name: a (string) name used for the tag/key for serialization or
     a callable(model) that returns a name
    :param property_map: a map of (field) names (string) -> types or a callable(model)
     that returns a map.
    """

    def wrap(cls):
        """
        Restler serialization class decorator for SqlAlchemy models
        """
        @classmethod
        def _restler_types(cls):
            """
            A map of types types to callables that serialize those types.
            """
            from sqlalchemy.types import Binary, Interval, LargeBinary, PickleType
            from sqlalchemy.orm.query import Query
            _type_map = create_type_map(type_map)
            _type_map.update({
                Query: lambda query: list(query),
                Binary: unsupported(Binary),
                Interval: unsupported(Interval),
                LargeBinary: unsupported(LargeBinary),
                PickleType: unsupported(PickleType)
            })
            return _type_map

        @classmethod
        def _restler_serialization_name(cls):
            """
            The lowercase model classname
            """
            _serialization_name = create_serialization_name(cls, serialization_name or cls.__name__.lower())
            return _serialization_name

        @classmethod
        def _restler_property_map(cls):
            """
            List of model property names -> property types. The names are used in
            *include_all_fields=True* Property must be from **sqlalchemy.types**
            """
            _property_map = create_property_map(cls, property_map)
            columns = cls.__table__.columns
            column_map = dict([(name, columns.get(name).type.__class__) for name in columns.keys()])
            _property_map.update(column_map)
            return _property_map

        wrap_method(cls, _restler_types)
        wrap_method(cls, _restler_property_map)
        cls._restler_serialization_name = _restler_serialization_name

        return cls
    return wrap

sqlalchemy_serializer = sqlalchemy_decorator_builder()
