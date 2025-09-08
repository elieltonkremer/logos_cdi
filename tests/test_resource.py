import pytest
from logos_cdi.resource import Parameter, Service, Singleton
from logos_cdi.reference import Reference
from logos_cdi.container import Container
from logos_cdi.context import Context

# Tests for Parameter resource
def test_parameter_resolves_static_value():
    param = Parameter("static_value")
    container = Container({})
    context = Context(container)
    assert param.resolve(context) == "static_value"

def test_parameter_resolves_nested_reference():
    param = Parameter({"key": Reference("another_param")})
    container = Container({"another_param": Parameter("nested_value")})
    context = Context(container)
    resolved = param.resolve(context)
    assert resolved == {"key": "nested_value"}

# Tests for Service resource
class MyService:
    def __init__(self, dependency):
        self.dependency = dependency

def test_service_instantiation():
    service = Service(
        class_path=f"{__name__}.MyService",
        parameters={"dependency": Reference("my_dependency")}
    )
    container = Container({
        "my_dependency": Parameter("dependency_value"),
        "my_service": service
    })
    context = Context(container)
    instance = service.resolve(context)
    assert isinstance(instance, MyService)
    assert instance.dependency == "dependency_value"

# Tests for Singleton resource
def test_singleton_creates_one_instance():
    singleton = Singleton(
        class_path=f"{__name__}.MyService",
        parameters={"dependency": Reference("my_dependency")}
    )
    container = Container({
        "my_dependency": Parameter("dependency_value"),
        "my_singleton": singleton
    })
    context = Context(container)

    instance1 = singleton.resolve(context)
    instance2 = singleton.resolve(context)

    assert isinstance(instance1, MyService)
    assert instance1 is instance2

def test_singleton_in_different_contexts():
    singleton = Singleton(
        class_path=f"{__name__}.MyService",
        parameters={"dependency": Reference("my_dependency")}
    )
    container = Container({
        "my_dependency": Parameter("dependency_value"),
        "my_singleton": singleton
    })

    context1 = Context(container)
    context2 = Context(container)

    instance1 = singleton.resolve(context1)
    instance2 = singleton.resolve(context2)

    assert instance1 is not instance2
