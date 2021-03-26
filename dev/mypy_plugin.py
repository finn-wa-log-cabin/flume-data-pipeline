from mypy.plugin import Plugin
from mypy.plugins import dataclasses


def plugin(version: str):
    return FixMarshamallowDataClassPlugin


class FixMarshamallowDataClassPlugin(Plugin):
    def get_class_decorator_hook(self, fullname: str):
        from mypy.plugins import dataclasses

        if fullname == "marshmallow_dataclass.dataclass":
            return dataclasses.dataclass_class_maker_callback
        return None
