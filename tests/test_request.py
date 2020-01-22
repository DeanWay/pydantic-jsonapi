from pytest import raises

from pydantic import ValidationError

from pydantic_jsonapi import JsonApiRequest
from tests.helpers import ItemModel


class TestJsonApiRequest:
    def test_attributes_as_dict(self):
        DictRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': {'type': 'item', 'attributes': {}}
        }
        my_request_obj = DictRequest(**obj_to_validate)
        assert my_request_obj.dict() == {
            'data': {
                'type': 'item',
                'attributes': {},
                'relationships': None,
                'id': None,
            }
        }

    def test_attributes_as_item_model(self):
        ItemRequest = JsonApiRequest('item', ItemModel)
        obj_to_validate = {
            'data': {
                'type': 'item',
                'attributes': {
                    'name': 'apple',
                    'quantity': 10,
                    'price': 1.20
                },
                'relationships': None,
                'id': None,
            }
        }
        my_request_obj = ItemRequest(**obj_to_validate)
        assert my_request_obj.dict() == obj_to_validate

    def test_attributes_not_required(self):
        MyRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': {
                'type': 'item',
                'attributes': None,
                'relationships': None,
                'id': None,
            }
        }
        my_request_obj = MyRequest(**obj_to_validate)
        assert my_request_obj.dict() == obj_to_validate

    def test_attributes_as_item_model__empty_dict(self):
        ItemRequest = JsonApiRequest('item', ItemModel)
        obj_to_validate = {
            'data': {
                'type': 'item',
                'attributes': {}
            }
        }
        with raises(ValidationError) as e:
            ItemRequest(**obj_to_validate)

        assert e.value.errors() == [
            {'loc': ('data', 'attributes', 'name'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 'attributes', 'quantity'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 'attributes', 'price'), 'msg': 'field required', 'type': 'value_error.missing'}
        ]

    def test_type_invalid_string(self):
        MyRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': {'type': 'not_an_item', 'attributes': {}}
        }
        with raises(ValidationError) as e:
            MyRequest(**obj_to_validate)

        assert e.value.errors() == [
            {
                'loc': ('data', 'type'),
                'msg': "unexpected value; permitted: 'item'",
                'type': 'value_error.const',
                'ctx': {'given': 'not_an_item', 'permitted': ('item',)},
            },
        ]

    def test_data_required(self):
        MyRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': None
        }
        with raises(ValidationError) as e:
            MyRequest(**obj_to_validate)

        assert e.value.errors() == [
            {'loc': ('data',), 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'},
        ]

    def test_request_with_relationships(self):
        MyRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': {
                'type': 'item',
                'attributes': {},
                'relationships': {
                    'sold_at': {
                        'data': {
                            'type': 'store',
                            'id': 'abc123',
                            'meta': None
                        },
                    }
                }
            },
        }
        my_request_obj = MyRequest(**obj_to_validate)
        assert my_request_obj.dict() == {
            'data': {
                'type': 'item',
                'attributes': {},
                'relationships': {
                    'sold_at': {
                        'data': {
                            'type': 'store',
                            'id': 'abc123',
                            'meta': None
                        },
                    }
                },
                'id': None
            },
        }

    def test_request_with_id(self):
        MyRequest = JsonApiRequest('item', dict)
        obj_to_validate = {
            'data': {
                'type': 'item',
                'attributes': {},
                'id': 'abc123'
            },
        }
        my_request_obj = MyRequest(**obj_to_validate)
        assert my_request_obj.dict() == {
            'data': {
                'type': 'item',
                'attributes': {},
                'relationships': None,
                'id': 'abc123',
            },
        }

