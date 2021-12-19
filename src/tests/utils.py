import decimal
import json
from collections import OrderedDict
from typing import Type

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.serializers import Serializer

from src.core.serialize_utils import get_serializer_data


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def get_dumped_json_serializer(serializer: Type[Serializer]) -> str:
    return json.dumps(
        obj=get_serializer_data(serializer),
        cls=DjangoJSONEncoder,
        default=decimal_default
    )

