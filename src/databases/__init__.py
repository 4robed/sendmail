import json

from redis import Redis as _Redis


class Redis(_Redis):
    def get(self, key):
        result = super().get(key)

        if result is None:
            return result

        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
        return result

    def set(self, key, value, **kwargs):

        if not isinstance(value, bytes):
            value = json.dumps(value)

        return super().set(key, value, **kwargs)


__all__ = (
    'Redis'
)
