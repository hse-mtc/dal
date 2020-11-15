import json

from rest_framework.parsers import MultiPartParser


class MultiPartWithJSONParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        daf = super().parse(stream, media_type, parser_context)
        daf.data = daf.data.copy()
        data = [json.loads(data) for data in daf.data.pop("data")]
        daf.data.setlist("data", data)
        return daf
