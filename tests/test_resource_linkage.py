import pytest
from pytest import raises

from pydantic_jsonapi.resource_linkage import ResourceLinkage
from pydantic import BaseModel, ValidationError


class ThingWithLinkageData(BaseModel):
    data: ResourceLinkage


class TestResourceLinks:

    @pytest.mark.parametrize(
        'linkage, message',
        [
            (
                None,
                'null is valid for empty to-one relationships',
            ),
            (
                [],
                'empty list valid for empty to-many relationships.',
            ),
            (
                {'id': 'abc123', 'type': 'item', 'meta': None},
                'single resource identifier valid for non-empty to-one relationships.',
            ),
            (
                [
                    {'id': 'abc123', 'type': 'item', 'meta': None},
                    {'id': 'def456', 'type': 'item', 'meta': None},
                ],
                'array of resource identifiers valid for non-empty to-many relationships.',
            ),
        ],
    )
    def test_valid_possibilities(self, linkage, message):
        structure_to_validate = {
            'data': linkage
        }
        validated = ThingWithLinkageData(**structure_to_validate)
        assert validated.dict() == structure_to_validate, message

    def test_invalid_resource_identifier(self):
        structure_to_validate = {
            'data': {}
        }
        with raises(ValidationError) as e:
            ThingWithLinkageData(**structure_to_validate)
        assert e.value.errors() == [
            {'loc': ('data', 'id'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 'type'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data',), 'msg': 'value is not a valid list', 'type': 'type_error.list'},
        ]

    def test_invalid_resource_identifier_array(self):
        structure_to_validate = {
            'data': [
                {}
            ],
        }
        with raises(ValidationError) as e:
            ThingWithLinkageData(**structure_to_validate)
        assert e.value.errors() == [
            {'loc': ('data',), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'},
            {'loc': ('data', 0, 'id'), 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ('data', 0, 'type'), 'msg': 'field required', 'type': 'value_error.missing'},
        ]
