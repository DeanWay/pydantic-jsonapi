from pytest import raises

from pydantic import ValidationError

from pydantic_jsonapi import Request, RequestData


class TestRequest:
    def test_needs_data_type(self):
        with raises(TypeError):
            Request(data={})

    def test_data_as_dict(self):
        MyRequest = Request[dict]
        my_request_obj = MyRequest(data={})
        assert my_request_obj.dict() == {'data': {}}

    def test_data_required(self):
        MyRequest = Request[dict]
        with raises(ValidationError):
            MyRequest(data=None)


class TestRequestData:
    def ttest_needs_attributes_type(self):
        with raises(TypeError):
            RequestData(type='abc', attributes={})

    def test_attributes_as_dict(self):
        MyRequestData = RequestData[dict]
        my_request_obj = MyRequestData(type='', attributes={})
        assert my_request_obj.dict() == {'type': '', 'attributes': {}}

    def test_attributes_required(self):
        MyRequestData = RequestData[dict]
        with raises(ValidationError):
            MyRequestData(type='', attributes=None)

    def test_type_required(self):
        MyRequestData = RequestData[dict]
        with raises(ValidationError):
            MyRequestData(type=None, attributes={})
