# -*- coding: utf-8 -*-

import importlib.util


def import_module(name):
    spec = importlib.util.spec_from_file_location(name, f'{name}.app.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# noinspection PyCallingNonCallable
class BaseLambdaTester:

    def __init__(self, module_name):
        self.lib = import_module(module_name)

    def set(self, key, val):
        if hasattr(self.lib, 'on_set'):
            self.lib.on_set(key, val)

    def set_dict(self, **kwargs):
        for key, val in kwargs.items():
            self.set(key, val)

    def get(self, key):
        if hasattr(self.lib, 'on_get'):
            return self.lib.on_get(key)
        else:
            return None

    def init(self):
        if hasattr(self.lib, 'on_init'):
            return self.lib.on_init()
        else:
            return True

    def valid(self):
        if hasattr(self.lib, 'on_valid'):
            return self.lib.on_valid()
        else:
            return True

    def run(self, *args, **kwargs):
        assert hasattr(self.lib, 'on_run')
        return self.lib.on_run(*args, **kwargs)

    def destroy(self):
        if hasattr(self.lib, 'on_destroy'):
            self.lib.on_destroy()


if __name__ == '__main__':
    pass
