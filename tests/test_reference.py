import pytest
from logos_cdi.reference import Reference, Parent, Decorated, Context as ContextRef, AllRegisteredReference
from logos_cdi.resource import Parameter, Service
from logos_cdi.container import Container
from logos_cdi.context import Context
from logos_cdi.registry import Registry

# Test for Reference
def test_reference_resolves_to_resource():
    ref = Reference("my_param")
    container = Container({"my_param": Parameter("value")})
    context = Context(container)
    assert ref.get(context) == "value"

# Test for Parent
def test_parent_reference():
    parent_container = Container({"parent_param": Parameter("parent_value")})
    parent_context = Context(parent_container)

    child_container = Container({})
    child_context = parent_context.nested(child_container)

    ref = Parent("parent_param")
    assert ref.get(child_context) == "parent_value"

def test_parent_reference_returns_none_if_not_found():
    container = Container({})
    context = Context(container)
    ref = Parent("non_existent")
    assert ref.get(context) is None

# Test for Decorated
class DecoratedService:
    def __init__(self, inner):
        self.inner = inner

def test_decorated_reference():
    container = Container({
        "original_service": Parameter("original"),
        "decorator": Service(
            class_path=f"{__name__}.DecoratedService",
            parameters={"inner": Decorated("original_service", Context(Container({})))}
        )
    })
    context = Context(container)

    # This is a simplified test. In a real scenario, the DI container
    # would inject the correct current_context into the Decorated reference.
    # For this test, we manually create a Decorated reference.
    decorated_ref = Decorated("original_service", context)
    decorated_instance = decorated_ref.get(context)
    assert decorated_instance == "original"

# Test for ContextRef
def test_context_reference():
    container = Container({})
    context = Context(container)
    ref = ContextRef()
    assert ref.get(context) is context

from logos_cdi.abstract import AbstractReference

# Test for AllRegisteredReference
def test_all_registered_reference():
    registry = Registry(parent=None, type=AbstractReference)
    registry.register("one", Reference("param_one"))
    registry.register("two", Reference("param_two"))

    container = Container({
        "my_registry": Parameter(registry),
        "param_one": Parameter(1),
        "param_two": Parameter(2)
    })
    context = Context(container)

    ref = AllRegisteredReference("my_registry")
    resolved = ref.get(context)
    assert resolved == {"one": 1, "two": 2}
