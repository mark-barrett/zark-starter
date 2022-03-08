import json
from json import JSONDecodeError
from typing import Any

from pydantic import BaseModel

from bs4 import BeautifulSoup

from zark.exceptions.serializing import SerializingException


class Schema(BaseModel):

    # Validated data
    instance: Any = None

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__()

    '''
        A Schema defines how a request payload becomes a Python Object and how a Python Object becomes a response payload
    '''
    def serialize(self):
        '''
            Serializes the Object to a String representation of itself
        :return:
        '''
        ...

    def deserialize(self):
        '''
            Deserializes the Object to a Python Object version of itself
        :return:
        '''
        ...


class JSONSchema(Schema):

    def __init__(self, request_payload: str):
        try:
            json_payload = json.loads(request_payload)
            super(Schema, self).__init__(**json_payload)
        except JSONDecodeError as exception:
            raise SerializingException(f"JSON not valid: {str(exception)}")

    def deserialize(self):
        # todo: add check here to only allow deserialize to be called if the instance var has been called
        return json.dumps(self.instance)


class XMLSchema(Schema):

    def __init__(self, request_payload: str):
        # todo: coming soon
        super(Schema, self).__init__(**request_payload)
        pass

