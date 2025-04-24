import logging
import re
from datetime import datetime
from email.utils import parseaddr
from collections.abc import Iterable


class Serializer:

    def __init__(self, source, rules, delimiter=',', verbosity=0):
        self.source = source
        self.rules = rules
        self.delimiter = delimiter
        self.verbosity = verbosity


    def __iter__(self):
        return self


    def __next__(self):
        while True:
            data = next(self.source)
            try:
                result = self.serialize(data)
                if self.verbosity > 2:
                    logging.debug(f"Serializer parsed: {result}")
                return result
            except Exception as e:
                logging.debug(f"Serializer skipped: {data}. Cause: {e}")
                

    def serialize(self, data):
        if isinstance(data, dict):
            return self.serialize_as_dict(data)
        elif isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
            return self.serialize_as_list(data)
        raise Exception("Data is neither a dict or an iterable")


    def serialize_as_dict(self, data):
        if self.verbosity > 2:
            logging.debug(f"Serializer serializing dict: {data}")
        for key, rule in self.rules.items():
            if key not in data:
                # Check if the parameters 'required' setting if False
                required = rule['params'].get('required', True)
                if required:
                    raise Exception(f"key '{key}' is not present.")
            else:
                data[key] = self.serialize_field(key, data[key], rule)
        return self.delimiter.join(data)


    def serialize_as_list(self, data):
        if self.verbosity > 2:
            logging.debug(f"Serializer serializing list: {data}")
        for index, (key, rule) in enumerate(self.rules.items()):
            data[index] = self.serialize_field(key, data[index], rule)
        return self.delimiter.join(data)


    def is_valid_field(self, key):
        return key in self.rules


    def serialize_field(self, key, value, val_data):
        # test the field on NoneType and validate nullable
        if value is None:
            return ''
        # find a parser method to call and call it
        method = self.get_parser_method(key, val_data['type'])
        return method(key, value, **val_data)


    def get_parser_method(self, key, type):
        func_name = 'serialize_' + type
        return getattr(self,func_name) 


    def serialize_str(self, key, value, **kwargs):
        return value


    def serialize_substr(self, key, value, **kwargs):
        return value

    def serialize_int(self, key, value, **kwargs):
        return str(value)


    def serialize_float(self, key, value, decimals=-1, **kwargs):
        if decimals < 0:
            return str(value)
        return f"{value:.{decimals}f}"


    def serialize_date(self, key, value, **kwargs):
        return self.parse_datetime(key, value, **kwargs)


    def serialize_datetime(self, key, value, format=None, **kwargs):
        if format is None:
            raise Exception("No date format found for {}[{}]".format(key, value))
        return value.strftime(format)


    def serialize_email(self, key, value, **kwargs):
        return value


