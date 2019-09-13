from pytest import raises

from pydantic_jsonapi.relationships import RelationshipsType
from pydantic import BaseModel, ValidationError


class Relatable(BaseModel):
    relationships: RelationshipsType


class TestRelationshipsType:
    def test_follows_strucutre(self):
        validated = Relatable(relationships={
            'walter': {
                'links': {
                    'self': '/person/walter'
                }
            },
            'wendy': {
                'links': {
                    'self': '/person/wendy'
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
                    'data': None,
                    'meta': None,
                }
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
