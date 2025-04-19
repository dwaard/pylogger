import logging
import re
from datetime import datetime
from email.utils import parseaddr
from collections.abc import Iterable


class Parser:

    def __init__(self, source, rules, verbosity=0):
        self.source = source
        self.rules = rules
        self.verbosity = verbosity


    def __iter__(self):
        return self


    def __next__(self):
        while True:
            data = next(self.source)
            try:
                result = self.parse(data)
                if self.verbosity > 2:
                    logging.debug(f"Parser parsed: {result}")
                return result
            except Exception as e:
                logging.debug(f"Parser skipped: {data}. Cause: {e}")


    def parse_as_dict(self, data):
        for key, rule in self.rules.items():
            if key not in data:
                # Check if the parameters 'required' setting if False
                required = rule['params'].get('required', True)
                if required:
                    raise Exception(f"key '{key}' is not present.")
            else:
                data[key] = self.parse_field(key, data[key], rule)
        return data


    def parse_as_list(self, data):
        for index, (key, rule) in enumerate(self.rules.items()):
            data[index] = self.parse_field(key, data[index], rule)
        return data


    def parse(self, data):
        if isinstance(data, dict):
            return self.parse_as_dict(data)
        elif isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
            return self.parse_as_list(data)
        raise Exception("Data is neither a dict or an iterable")

    def is_valid_field(self, key):
        return key in self.rules


    def parse_field(self, key, value, val_data):
        # test the field on NoneType and validate nullable
        if self.parse_none(key, value, **self.get_params(val_data)):
            return None
        # find a parser method to call and call it
        method = self.get_parser_method(key, val_data['type'])
        return method(key, value, **self.get_params(val_data))


    def get_params(self, val_data):
        if 'params' not in val_data:
            return {}
        return val_data['params']


    def get_parser_method(self, key, type):
        func_name = 'parse_' + type
        return getattr(self,func_name) 


    def parse_none(self, key, value, **kwargs):
        # test if value is None-like
        is_none = False
        if self.is_none_like(value):
            is_none = True
        # test if it is allowed to be None
        if is_none and ('nullable' not in kwargs or kwargs['nullable']==False):
            raise Exception('Field {}[value:{}] is not allowed to be of NoneType'.format(key, value))
        return is_none


    def is_none_like(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            return len(value)==0 or value=='NULL'
        return False


    def parse_str(self, key, value, **kwargs):
        if 'pattern' in kwargs:
            pattern = kwargs['pattern']
            if not re.fullmatch(pattern, value):
                raise Exception(f"{key} with value {value} does not match the {pattern} pattern")
        return value


    def parse_substr(self, key, value, **kwargs):
        if 'start' not in kwargs:
            raise Exception('start param must be present in substr validator')
        start_index = value.find(kwargs['start'])
        if start_index<0:
            raise Exception('start string {} not found in {}'.format(kwargs['start'], value))
        if 'end' not in kwargs:
            raise Exception('end param must be present in substr validator')
        end_index = value.find(kwargs['end'], start_index)
        if end_index<0:
            raise Exception('end string {} not found in {}'.format(kwargs['end'], value))
        logging.debug('indices: {} - {}'.format(start_index, end_index))
        return value[start_index+1:end_index-len(value)]


    def parse_int(self, key, value, **kwargs):
        try:
            intval = int(value)
        except:
            raise Exception("{} is not a valid int for {}".format(value, key))
        if 'min' in kwargs:
            if intval < kwargs['min']:
                raise Exception("{} is too low for {}".format(value, key))
        if 'max' in kwargs:
            if intval > kwargs['max']:
                raise Exception("{} is too high for {}".format(value, key))
        return intval


    def parse_float(self, key, value, **kwargs):
        try:
            floatval = float(value)
        except:
            raise Exception("{} is not a valid float for {}".format(value, key))
        if 'min' in kwargs:
            if floatval < kwargs['min']:
                raise Exception("{} is too low for {}".format(value, key))
        if 'max' in kwargs:
            if floatval > kwargs['max']:
                raise Exception("{} is too high for {}".format(value, key))
        return floatval


    def parse_date(self, key, value, **kwargs):
        if 'format' not in kwargs:
            raise Exception("No dat format found for {}[{}]".format(key, value))
        return datetime.strptime(value, kwargs['format'])


    def parse_email(self, key, value, **kwargs):
        return parseaddr(value)[1]


