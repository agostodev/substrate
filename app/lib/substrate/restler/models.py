class TransientModel(object):
    """A helper class that can be used to transform external services into
    restler services. Any subclass can be used with a ModelStrategy. Override
    the required_fields and optional_fields and instantiate using init parameters.
    e.g. MyTransientModel(field1=val1, field2=val2...)
    """

    @classmethod
    def _restler_serialization_name(cls):
        """
        :return: name to use in the serialized output for this object
        """
        return cls.__name__

    @classmethod
    def required_fields(cls):
        """
        :return: A tuple of (str) names of attributes that are required.
        """
        return tuple()

    @classmethod
    def optional_fields(cls):
        """
        :return: A tuple of (str) names of attributes that are option.
        """
        return tuple()

    @classmethod
    def _restler_property_map(cls):
        """
        :return: fields that can be serialized.  Also used with `include_all_fields`
        """
        return dict([(name, name.__class__) for name in cls.required_fields() + cls.optional_fields()])

    @classmethod
    def fields(cls):
        return cls.required_fields() + cls.optional_fields()

    @classmethod
    def _restler_types(cls):
        """
        :return: a map of types -> callables, for any types that can't be serialized
         automatically to JSON. The callable should transform an instance into a value
         e.g. string, number, list that can be serialized by a JSON encoder.
        The format e.g. is {MyType: lambda instance_of_type: str(instance_of_type, ...}
        """
        return {}

    def __init__(self, **kwargs):
        for prop in self._restler_property_map().keys():
            setattr(self, prop, kwargs.get(prop))
            if prop in self.required_fields() and getattr(self, prop) is None:
                raise AttributeError('The property: %s is required.' % prop)

    def properties(self):
        """
        :return: a dictionary of key/value pairs for fields in this model
        """
        return dict([(prop, getattr(self, prop)) for prop in self.fields()])
