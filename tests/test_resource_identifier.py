from pytest import raises
from pydantic import ValidationError

from pydantic_jsonapi.resource_identifier import ResourceIdentifier

class TestResourceIdentifier:
    def test_follows_strucutre(self):
        structure_to_validate = {
            'id': 'abc123',
            'type': 'item',
            'meta': {
                'set': 'of',
                'extra': 'data',
            },
        }
        validated = ResourceIdentifier(**structure_to_validate)
        assert validated.dict() == structure_to_validate

    def test_required_fields(self):
        with raises(ValidationError) as e:
            ResourceIdentifier()
        assert e.value.errors() == [
            {'loc': ('id',), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('type',), 'msg': 'field required', 'type': 'value_error.missing'},
        ]

    def test_meta_must_be_dict(self):
        with raises(ValidationError) as e:
            ResourceIdentifier(
                id='abc123',
                type='item',
                meta=['123']
            )
        assert e.value.errors() == [
            {'loc': ('meta',), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'},
            {'loc': ('meta',), 'msg': 'value is not none', 'type': 'type_error.none.allowed'}
        ]
