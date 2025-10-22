import json

from rest_framework.parsers import MultiPartParser


class MultiPartWithJSONParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        # pylint: disable=too-many-locals

        daf = super().parse(stream, media_type, parser_context)

        # `.data` is immutable QueryDict, `.copy()` will make it mutable
        daf.data = daf.data.copy()

        raw_data = daf.data.pop("data", None)

        # No data was sent (only files), skip JSON parsing
        if raw_data is None:
            return daf

        data = [json.loads(fields) for fields in raw_data]

        # Data contains fields for more than one object, preserve list structure
        if len(data) > 1:
            daf.data.setlist("data", data)

        # Set all fields manually so other methods won't fail
        if len(data) == 1:
            for key, value in data[0].items():
                if isinstance(value, list):
                    daf.data.setlist(key, value)
                elif isinstance(value, dict):
                    daf.data[key] = json.dumps(value)
                else:
                    daf.data[key] = value

        return daf
