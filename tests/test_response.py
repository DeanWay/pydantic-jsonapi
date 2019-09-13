from pytest import raises

from pydantic import BaseModel, ValidationError

from pydantic_jsonapi import JsonApiResponse
from tests.helpers import ItemModel


class TestJsonApiResponse:
    def test_attributes_as_dict(self):
        MyResponse = JsonApiResponse('item', dict)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'item', 'attributes': {}}
        }
        my_request_obj = MyResponse(**obj_to_validate)
        assert my_request_obj.dict() == {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {},
                'relationships': None,
            },
            'errors': None,
            'included': None,
            'links': None,
            'meta': None,
        }

    def test_attributes_as_item_model(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        obj_to_validate = {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {
                    'name': 'apple',
                    'quantity': 10,
                    'price': 1.20
                },
                'relationships': {
                    'store': {
                        'links': {
                            'related': '/stores/123',
                        },
                    },
                },
            }
        }
        my_request_obj = ItemResponse(**obj_to_validate)
        assert my_request_obj.dict() == {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {
                    'name': 'apple',
                    'quantity': 10,
                    'price': 1.20,
                },
                'relationships': {
                    'store': {
                        'links': {
                            'related': '/stores/123',
                        },
                        'data': None,
                        'meta': None,
                    },
                },
            },
            'errors': None,
            'included': None,
            'links': None,
            'meta': None,
        }

    def test_type_invalid_string(self):
        MyResponse = JsonApiResponse('item', dict)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'not_an_item', 'attributes': {}}
        }
        with raises(ValidationError) as e:
            MyResponse(**obj_to_validate)

        assert e.value.errors() == [
            {
                'loc': ('data', 'type'),
                'msg': "unexpected value; permitted: 'item'",
                'type': 'value_error.const',
                'ctx': {'given': 'not_an_item', 'permitted': ('item',)},
            },
            {
                'loc': ('data',),
                'msg': 'value is not none',
                'type': 'type_error.none.allowed',
            },
        ]

    def test_attributes_required(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'item', 'attributes': None}
        }
        with raises(ValidationError) as e:
            ItemResponse(**obj_to_validate)

        assert e.value.errors() == [
            {
                'loc': ('data', 'attributes'),
                'msg': 'value is not a valid dict',
                'type': 'type_error.dict',
            },
            {
                'loc': ('data',),
                'msg': 'value is not none',
                'type': 'type_error.none.allowed',
            },
        ]

    def test_attributes_as_item_model__empty_dict(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        obj_to_validate = {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {}
            }
        }
        with raises(ValidationError) as e:
            ItemResponse(**obj_to_validate)

        assert e.value.errors() == [
            {'loc': ('data', 'attributes', 'name'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 'attributes', 'quantity'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 'attributes', 'price'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data',), 'msg': 'value is not none', 'type': 'type_error.none.allowed'},
        ]
