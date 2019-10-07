from pytest import raises

from pydantic import BaseModel, ValidationError

from pydantic_jsonapi import JsonApiResponse
from tests.helpers import ItemModel


class TestJsonApiResponse:
    def test_attributes_as_dict(self):
        MyResponse = JsonApiResponse('item', dict)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'item', 'attributes': {}},
            'included': [{'id': '456', 'type': 'not-an-item', 'attributes': {}}]
        }
        my_response_object = MyResponse(**obj_to_validate)
        assert my_response_object.dict() == {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {},
            },
            'included': [{
                'id': '456',
                'type': 'not-an-item',
                'attributes': {}
            }]
        }

    def test_missing_attributes_dict(self):
        MyResponse = JsonApiResponse('item', dict)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'item'}
        }
        my_response_object = MyResponse(**obj_to_validate)
        assert my_response_object.dict() == {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {},
            }
        }

    def test_missing_attributes_empty_model(self):
        class EmptyModel(BaseModel):
            pass

        MyResponse = JsonApiResponse('item', EmptyModel)
        obj_to_validate = {
            'data': {'id': '123', 'type': 'item'}
        }
        my_response_object = MyResponse(**obj_to_validate)
        assert my_response_object.dict() == {
            'data': {
                'id': '123',
                'type': 'item',
                'attributes': {},
            }
        }
        assert isinstance(my_response_object.data.attributes, EmptyModel)

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
        my_response_obj = ItemResponse(**obj_to_validate)
        assert my_response_obj.dict() == {
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
                    },
                },
            },
        }

    def test_list_item_model(self):
        ItemResponse = JsonApiResponse('item', ItemModel, use_list=True)
        obj_to_validate = {
            'data': [
                {
                    'id': '123',
                    'type': 'item',
                    'attributes': {
                        'name': 'apple',
                        'quantity': 10,
                        'price': 1.20
                    },
                },
                {
                    'id': '321',
                    'type': 'item',
                    'attributes': {
                        'name': 'banana',
                        'quantity': 20,
                        'price': 2.34
                    },
                },
            ],
        }
        my_response_obj = ItemResponse(**obj_to_validate)
        assert my_response_obj.dict() == {
            'data': [
                {
                    'id': '123',
                    'type': 'item',
                    'attributes': {
                        'name': 'apple',
                        'quantity': 10,
                        'price': 1.20,
                    },
                },
                {
                    'id': '321',
                    'type': 'item',
                    'attributes': {
                        'name': 'banana',
                        'quantity': 20,
                        'price': 2.34,
                    },
                },
            ],
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
        ]
