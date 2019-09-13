from pytest import raises

from pydantic_jsonapi.links import LinksType
from pydantic import BaseModel, ValidationError


class ThingWithLinks(BaseModel):
    links: LinksType


class TestLinksType:
    def test_follows_strucutre(self):
        structure_to_validate = {
            'links': {
                'self': '/person/walter',
                'related': {
                    'href': '/person/wendy',
                    'meta': {
                        'relationship': 'friend',
                    },
                }
            }
        }
        validated = ThingWithLinks(**structure_to_validate)
        assert validated.dict() == structure_to_validate

    def test_must_be_valid_map(self):
        with raises(ValidationError) as e:
            ThingWithLinks(links=['walter', 'wendy'])
        assert e.value.errors() == [
            {'loc': ('links',), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'}
        ]

    def test_values_must_be_a_str_or_link_href_object(self):
        ThingWithLinks(links={'walter': ''})
        ThingWithLinks(links={
            'wendy': {
                'href': '/person/wendy',
                'meta': {
                    'relationship': 'friend',
                },
            }
        })
        invalid_string_error = {'loc': ('links', 'walter'), 'msg': 'str type expected', 'type': 'type_error.str'}

        with raises(ValidationError) as e:
            ThingWithLinks(links={'walter': object()})
        assert e.value.errors() == [
            invalid_string_error,
            {'loc': ('links', 'walter'), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'}
        ]

        with raises(ValidationError) as e:
            ThingWithLinks(links={'walter': {'href': '/people/123'}})
        assert e.value.errors() == [
            invalid_string_error,
            {'loc': ('links', 'walter', 'meta'), 'msg': 'field required', 'type': 'value_error.missing'},
        ]
