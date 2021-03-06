import sys

main_name = sys.argv[0]
if 'gui_app.py' in main_name:
    from tkinter.messagebox import showerror


class EntryValue:
    def __init__(self, value):
        self._value = value

    @classmethod
    def get_value(cls, obj):
        if isinstance(obj, cls):
            return obj.value
        else:
            return obj

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return repr(self._value)

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        self._value = value


if 'gui_app.py' in main_name:

    class EntryValueFactory:
        def create(self, value, dtype, widget_set):
            if dtype == 'float':
                return FloatEntryValue(value, widget_set)
            elif dtype == 'int':
                return IntEntryValue(value, widget_set)
            elif dtype == 'string':
                return StringEntryValue(value, widget_set)
            elif dtype in ('boolean', 'bool'):
                return BooleanEntryValue(value, widget_set)
            else:
                raise NotImplementedError

    class FloatEntryValue(EntryValue):

        def __init__(self, value, widget_set=None):
            try:
                value = float(value)
            except (ValueError, TypeError) as e:
                value = 0.0
            super().__init__(value)


    class IntEntryValue(EntryValue):

        def __init__(self, value, widget_set=None):
            try:
                value = int(value)
            except ValueError:
                if widget_set is None:
                    raise ValueError
                else:
                    showerror(title="Error",
                              message="int value must be provided "
                              "for {}".format(widget_set.name))
            # return super(FloatEntryValue, cls).__new__(cls, value)
            super().__init__(value)


    class StringEntryValue(EntryValue):
        def __init__(self, value, widget_set=None):
            super().__init__(value)


    class BooleanEntryValue(EntryValue):

        def __init__(self, value, widget_set=None):
            try:
                value = bool(value)
            except ValueError:
                if widget_set is None:
                    raise ValueError
                else:
                    showerror(title="Error",
                              message="bool value must be provided "
                              "for {}".format(widget_set.name))
            # return super(FloatEntryValue, cls).__new__(cls, value)
            super().__init__(value)
