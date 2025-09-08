from logos_cdi.application import Application, BaseModule
from logos_cdi.resource import Parameter
from logos_cdi.container import Container

class TestModule(BaseModule):
    def define_context(self, context):
        return context.nested(Container({
            'test_param': Parameter('test_value')
        }))

def test_application_initialization():
    app = Application(modules=[])
    assert app.has('application') is True
    assert app.get('application') is app

def test_application_with_modules():
    app = Application(modules=[TestModule()])
    assert app.has('test_param') is True
    assert app.get('test_param') == 'test_value'

def test_application_extends():
    app1 = Application(modules=[])

    class AnotherModule(BaseModule):
        def define_context(self, context):
            return context.nested(Container({
                'another_param': Parameter('another_value')
            }))

    app2 = app1.extends([AnotherModule()])

    assert app1.has('another_param') is False
    assert app2.has('application') is True
    assert app2.has('another_param') is True
    assert app2.get('another_param') == 'another_value'
