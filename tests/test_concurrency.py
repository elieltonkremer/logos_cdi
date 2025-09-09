import pytest
import threading
from logos_cdi.resource import Singleton, Service, Parameter
from logos_cdi.reference import Reference
from logos_cdi.container import Container
from logos_cdi.context import Context

class MyConcurrentService:
    def __init__(self, dep=None):
        self.dep = dep

def test_singleton_concurrency():
    """Tests that a Singleton is instantiated only once under concurrent access."""
    singleton = Singleton(class_path=f"{__name__}.MyConcurrentService", parameters={})
    container = Container({"my_singleton": singleton})
    context = Context(container)

    results = []
    def worker():
        instance = singleton.resolve(context)
        results.append(instance)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 10
    first_instance = results[0]
    assert all(instance is first_instance for instance in results)

def test_service_concurrency():
    """Tests that a Service is resolved correctly under concurrent access."""
    service = Service(class_path=f"{__name__}.MyConcurrentService", parameters={})
    container = Container({"my_service": service})
    context = Context(container)

    results = []
    errors = []
    def worker():
        try:
            instance = service.resolve(context)
            results.append(instance)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 10
    # Because of ContextVar and copy_context(), each thread gets its own context copy,
    # so each should get a different instance of the service.
    assert len(set(results)) == 10

def test_parameter_concurrency():
    """Tests that a Parameter with nested references is resolved correctly under concurrent access."""
    param = Parameter({"value": Reference("dependency")})
    container = Container({
        "my_param": param,
        "dependency": Parameter("dep_value")
    })
    context = Context(container)

    results = []
    errors = []
    def worker():
        try:
            resolved_value = param.resolve(context)
            results.append(resolved_value)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 10
    expected_value = {"value": "dep_value"}
    assert all(res == expected_value for res in results)
