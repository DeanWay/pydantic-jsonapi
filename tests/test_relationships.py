from pytest import raises

from pydantic_jsonapi.relationships import ResponseRelationshipsType
from pydantic import BaseModel, ValidationError


class Relatable(BaseModel):
    relationships: ResponseRelationshipsType


class TestResponseRelationshipsType:
    def test_follows_strucutre(self):
        validated = Relatable(relationships={
            'walter': {
                'data': None,
                'links': {
                    'self': '/person/walter'
                }
            },
            'wendy': {
                'data': {
                    'id': '1',
                    'type': 'wendy-type'
                },
                'links': {
                    'self': '/person/wendy'
                }
            },
            'wandas': {
                'data': [],
                'links': {
                    'self': '/person/wandas'
                }
            },
            'warners': {
                'data': [{
                    'id': '1',
                    'type': 'warner-type'
                }],
                'links': {
                    'self': '/person/warners'
                }
            }
        })
        assert validated.dict() == {
            'relationships': {
                'walter': {
                    'links': {
                        'self': '/person/walter'
                    },
                    'data': None,
                    'meta': None,
                },
                'wendy': {
                    'links': {
                        'self': '/person/wendy'
                    },
                    'data': {
                        'id': '1',
                        'type': 'wendy-type',
                        'meta': None,
                    },
                    'meta': None,
                },
                'wandas': {
                    'links': {
                        'self': '/person/wandas'
                    },
                    'data': [],
                    'meta': None,
                },
                'warners': {
                    'links': {
                        'self': '/person/warners'
                    },
                    'data': [{
                        'id': '1',
                        'type': 'warner-type',
                        'meta': None,
                    }],
                    'meta': None,
                },
            }
        }

    def test_must_be_valid_map(self):
        with raises(ValidationError) as e:
            Relatable(relationships=['walter', 'wendy'])
        assert e.value.errors() == [
            {'loc': ('relationships',), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'}
        ]

    def test_values_must_be_a_relationship_object(self):
        with raises(ValidationError) as e:
            Relatable(relationships={'walter': '/person/walter'})
        assert e.value.errors() == [
            {'loc': ('relationships', 'walter'), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'}
        ]
