# -*- coding: utf-8 -*-

import re
import functools

class Validator(object):
    """Base validator class"""
    def __init__(self, base=None):
        self.base = base

    def validate(self, test):
        return True

    def required_message(self, param_name):
        print('*** Parameter Error: parameter "%s" is required.\n' %param_name)

    def invalid_message(self, param_name, param_value=None):
        print('*** Parameter Error: invalid parameter "%s".\n' %param_name)


class Choice(Validator):
    """Validator for choosing an option from a list"""
    def validate(self, test):
        return (test in self.base)

    def invalid_message(self, param_name, param_value=None):
        print('*** Parameter Error: parameter "%s" must in %s, but "%s" got.\n'
            %(param_name, self.base, param_value))


class Equal(Validator):
    """Validator for exactly equal"""
    def validate(self, test):
        return test == self.base


class Regex(Validator):
    """Validator for regex matching"""
    def __init__(self, pattern):
        self.base = re.compile(pattern) if type(pattern)==str else pattern

    def validate(self, test):
        return self.base.match(test) != None

    def invalid_message(self, param_name, param_value=None):
        print('*** Parameter Error: parameter "%s" must match regex: %s.\n'
            %(param_name, self.base.pattern))


class FromObj(object):
    """Help decorator to dynamicly get parameters from an obj"""
    def __init__(self, func):
        self.func = func

    def generate(self, obj):
        return self.func(obj)


def parameter(name, required=False, validator=None, special_type=None):
    def decorator(method):
        # print('In method: %s -- %s' %(method.__name__, validator))
        @functools.wraps(method)
        def wrapper(obj, line, parsed_params=None):
            # 多级 parameter 装饰器串联时，接收上一级已经解析好的参数
            if parsed_params == None:
                parsed_params = []
            params = line.split() if type(line)==str else line

            # parameter_over 装饰器阻止解析接下来的参数
            if special_type == '__over__':
                if params:
                    print('*** Ignored excess parameters: %s\n' %params)
                return method(obj, *parsed_params)

            # 有些 validator 需要根据 obj 动态生成的
            if validator == None:
                vld = Validator()
            elif type(validator) in (tuple, list):
                cls, from_obj = validator[:2]
                vld = cls(from_obj.generate(obj))
            else:
                vld = validator

            # parameter_vary 装饰器将后面所有的参数作为一个可变长度的参数取走
            if special_type == '__vary__':
                for p in params:
                    if not vld.validate(p):
                        vld.invalid_message(name, p)
                        return
                parsed_params.append(params)
                return method(obj, *parsed_params)

            # 从 line 中解析出一个参数，如果参数为空且非必需，则设为默认值 ''
            p = ''
            if not line:
                if required:
                    vld.required_message(name)
                    return
            else:
                p = params[0]

            # 如果参数为必须或者参数虽可选但是用户指定了值，则需要进行参数合法性检查
            need_validate = required or (p != '')
            if need_validate and (not vld.validate(p)):
                vld.invalid_message(name, p)
                return

            # 多级 parameter 装饰器串联时，进入下一级
            parsed_params.append(p)
            line = params[1:] if len(params)>1 else []
            return method(obj, line, parsed_params)
        return wrapper
    return decorator


def parameter_over(**kw):
    if 'name' not in kw:
        kw['name'] = ''
    return parameter(special_type = '__over__', **kw)

def parameter_vary(**kw):
    if 'name' not in kw:
        kw['name'] = ''
    return parameter(special_type = '__vary__', **kw)
