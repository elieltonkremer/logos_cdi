import pytest
from logos_cdi.container import Container
from logos_cdi.resource import Parameter
from logos_cdi.error import ResourceNotFoundException

def test_container_has_resource():
    container = Container({'param': Parameter('value')})
    assert container.has('param') is True
    assert container.has('nonexistent') is False

from logos_cdi.context import Context

def test_container_get_resource():
    container = Container({'param': Parameter('value')})
    context = Context(container)
    assert container.get('param', context) == 'value'

def test_container_get_nonexistent_resource_raises_exception():
    container = Container({})
    with pytest.raises(ResourceNotFoundException):
        container.get('nonexistent')
