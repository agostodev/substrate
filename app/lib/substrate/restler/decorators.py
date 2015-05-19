

def ae_common_encoder(obj):
    """
    Common type specific encoders for app engine
    """
    from google.appengine.api import users
    if isinstance(obj, users.User):
        return obj.user_id() or obj.email()


def ae_common_extra_types(obj):
    """
    Non-core python or app engine specific types that can be serialized
    """
    from webapp2 import cached_property
    if isinstance(obj, cached_property):
        return True
    else:
        return False


def ae_db_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.db.Model for serialization
    """
    from google.appengine.ext import blobstore, db

    @classmethod
    def restler_collection_types(cls, obj):
        """
        Allows Restler to handle a collection type by retrieving the models
        """
        if isinstance(obj, db.Query):
            return True
        else:
            return False

    @classmethod
    def restler_encoder(cls, obj):
        """
        Type specific encoders
        """
        if isinstance(obj, db.GeoPt):
            return "%s %s" % (obj.lat, obj.lon)
        if isinstance(obj, db.IM):
            return "%s %s" % (obj.protocol, obj.address)
        if isinstance(obj, blobstore.BlobInfo):
            return str(obj.key())  # TODO is this correct?
        if ae_common_encoder(obj):
            return ae_common_encoder(obj)

    @classmethod
    def restler_kind(cls, model):
        """
        The lowercase model classname
        """
        return model.kind().lower()

    @classmethod
    def restler_properties(cls, model):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.db.Property**
        """
        return list(model.properties().iterkeys())

    @classmethod
    def restler_extra_types(cls, obj):
        """
        Non-core python or app engine specific types that can be serialized
        """
        return ae_common_extra_types(obj)

    cls.restler_collection_types = restler_collection_types
    cls.restler_encoder = restler_encoder
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties
    cls.restler_extra_types = restler_extra_types

    return cls


def ae_ndb_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.ndb.Model for serialization
    """
    from google.appengine.ext import ndb

    @classmethod
    def restler_collection_types(cls, obj):
        """
        Allows Restler to handle a collection type by retrieving the models
        """
        if isinstance(obj, ndb.query.Query):
            return True
        else:
            return False

    @classmethod
    def restler_encoder(cls, obj):
        """
        Type specific encoders
        """
        if isinstance(obj, ndb.GeoPt):
            return "%s %s" % (obj.lat, obj.lon)
        if ae_common_encoder(obj):
            return ae_common_encoder(obj)

    @classmethod
    def restler_kind(cls, model):
        """
        The lowercase model classname
        """
        try:
            return model.__class__.__name__.lower()
        except:
            # TODO When is this the case?
            return model.__name__.lower()

    @classmethod
    def restler_properties(cls, model):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.ndb.Property**
        """
        return list(model._properties.iterkeys())

    @classmethod
    def restler_extra_types(cls, obj):
        """
        Non-core python or app engine specific types that can be serialized
        """
        return ae_common_extra_types(obj)

    cls.restler_collection_types = restler_collection_types
    cls.restler_encoder = restler_encoder
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties
    cls.restler_extra_types = restler_extra_types

    return cls
