from dataclasses import dataclass
from datetime import datetime

from pytest import raises
from pydantic import BaseModel, ValidationError

from pydantic_jsonapi import JsonApiResponse
from tests.helpers import ItemModel, ItemModelWithOrmMode


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
                'msg': 'none is not an allowed value',
                'type': 'type_error.none.not_allowed',
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

    def test_resource_object_constructor(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        item = ItemModel(name='pear', price=1.2, quantity=10)
        document = ItemResponse.resource_object(id='abc123', attributes=item).dict()
        assert document == {
            'id': 'abc123',
            'type': 'item',
            'attributes': {
                'name': 'pear',
                'price': 1.2,
                'quantity': 10,
            },
            'relationships': None
        }

    def test_resource_object_constructor__no_attributes(self):
        IdentifierResponse = JsonApiResponse('item', dict)
        document = IdentifierResponse.resource_object(id='abc123').dict()
        assert document == {
            'id': 'abc123',
            'type': 'item',
            'attributes': {},
            'relationships': None
        }


    def test_resource_object_constructor__with_relationships(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        item = ItemModel(name='pear', price=1.2, quantity=10)
        document = ItemResponse.resource_object(
            id='abc123',
            attributes=item,
            relationships={
                'sold_at': {
                    'data': {'type': 'store', 'id': 'def456'}
                }
            }
        ).dict()
        assert document == {
            'id': 'abc123',
            'type': 'item',
            'attributes': {
                'name': 'pear',
                'price': 1.2,
                'quantity': 10,
            },
            'relationships': {
                'sold_at': {
                    'data': {
                        'id': 'def456',
                        'type': 'store',
                        'meta': None,
                    },
                    'links': None,
                    'meta': None,
                }
            }
        }

    def test_resource_object_constructor__with_invalid_relationship(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        item = ItemModel(name='pear', price=1.2, quantity=10)
        with raises(ValidationError) as e:
            ItemResponse.resource_object(
                id='abc123',
                attributes=item,
                relationships={
                    'sold_at': {
                        'meta': 'rofl'
                    }
                }
            )
        assert e.value.errors() == [
            {
                'loc': ('relationships', 'sold_at', 'meta'),
                'msg': 'value is not a valid dict',
                'type': 'type_error.dict'
            },
        ]

    def test_resource_object_constructor__with_list_response(self):
        ItemResponse = JsonApiResponse('item', ItemModel, use_list=True)
        item = ItemModel(name='pear', price=1.2, quantity=10)
        document = ItemResponse.resource_object(id='abc123', attributes=item).dict()
        assert document == {
            'id': 'abc123',
            'type': 'item',
            'attributes': {
                'name': 'pear',
                'price': 1.2,
                'quantity': 10,
            },
            'relationships': None
        }

    def test_response_constructed_with_resource_object(self):
        ItemResponse = JsonApiResponse('item', ItemModel)
        item = ItemModel(name='pear', price=1.2, quantity=10)
        data = ItemResponse.resource_object(id='abc123', attributes=item).dict()
        assert ItemResponse(data=data).dict() == {
            'data': {
                'id': 'abc123',
                'type': 'item',
                'attributes': {
                    'name': 'pear',
                    'price': 1.2,
                    'quantity': 10,
                },
            }
        }

    def test_response_constructed_with_resource_object__list(self):
        @dataclass
        class FakeDBItem:
            item_id: int
            name: str
            price: float
            quantity: int
            created_at: datetime = datetime.utcnow()

        ItemResponse = JsonApiResponse('item', ItemModelWithOrmMode, use_list=True)
        items = [
            FakeDBItem(item_id=1, name='apple', price=1.5, quantity=3),
            FakeDBItem(item_id=2, name='pear', price=1.2, quantity=10),
            FakeDBItem(item_id=3, name='orange', price=2.2, quantity=5)
        ]
        response = ItemResponse(
            data=[
                ItemResponse.resource_object(id=item.item_id, attributes=item)
                for item in items
            ]
        )
        assert response.dict() == {
            'data': [
                {
                    'id': '1',
                    'type': 'item',
                    'attributes': {
                        'name': 'apple',
                        'price': 1.5,
                        'quantity': 3,
                    },
                },
                {
                    'id': '2',
                    'type': 'item',
                    'attributes': {
                        'name': 'pear',
                        'price': 1.2,
                        'quantity': 10,
                    },
                },
                {
                    'id': '3',
                    'type': 'item',
                    'attributes': {
                        'name': 'orange',
                        'price': 2.2,
                        'quantity': 5,
                    },
                },
            ]
        }
