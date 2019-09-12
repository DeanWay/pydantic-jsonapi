from pytest import raises

from pydantic import ValidationError

from pydantic_jsonapi import Response, ResponseData


class TestResponse:
    def test_needs_data_type(self):
        with raises(TypeError):
            Response(data={})

    def test_data_as_dict(self):
        MyResponse = Response[dict]
        my_response_obj = MyResponse(data={})
        assert my_response_obj.dict() == {
            'data': {},
            'links': None,
            'meta': None,
            'included': None,
            'errors': None,
        }

    def test_data_as_list(self):
        MyResponse = Response[list]
        my_response_obj = MyResponse(data=[])
        assert my_response_obj.dict() == {
            'data': [],
            'links': None,
            'meta': None,
            'included': None,
            'errors': None,
        }


class TestResponsetData:
    def test_needs_attributes_type(self):
        with raises(TypeError):
            ResponseData(id='123', type='abc', attributes={})

    def test_attributes_as_dict(self):
        MyResponseData = ResponseData[dict]
        my_response_obj = MyResponseData(id='123', type='abc', attributes={})
        assert my_response_obj.dict() == {'id': '123', 'type': 'abc', 'attributes': {}, 'relationships': None}

    def test_attributes_required(self):
        MyResponseData = ResponseData[dict]
        with raises(ValidationError):
            MyResponseData(id='123', type='abc', attributes=None)

    def test_type_required(self):
        MyResponseData = ResponseData[dict]
        with raises(ValidationError):
            MyResponseData(id='123', type=None, attributes={})
