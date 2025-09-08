# logos_cdi

LogosCDI is a dependency injection tool that allows you to create extensible and maintainable applications


## How to install
```sh
pip install logos_cdi
```

## Basic usage
First you need to create an object of the Application class
```py
from logos_cdi.application import Application

app = Application(
    modules=[

    ]
)
```
You may want to use some modules to improve productivity
```py
from logos_cdi.application import Application
from logos_cdi.command import Commands

app = Application(
    modules=[
        Commands()
    ]
)
```
The Commands Module gives you a basis for creating commands to be executed in the terminal.

You can call it with:

```sh
$ logos
usage: logos [--app-url APP_URL] {} ...
logos: error: the following arguments are required: command
```
Create your own modules with commands

```py
from logos_cdi.command import Commands, AbstractCommand, CommandModule

class TestCommand(AbstractCommand):

    def define_arguments(self, argument_parser):
        argument_parser.add_argument('--name', default='Anonymous')
        return super().define_arguments(argument_parser)

    def execute(self):
        return print('Hello', self.arguments.name)

class Tests(CommandModule, BaseModule):

    def define_commands(self):
        return {
            'test': Service(
                class_path='test_module.TestCommand',
                parameters={}
            )
        }

```
Add to your application

```py
from logos_cdi.application import Application
from logos_cdi.command import Commands
from test_module import Tests

app = Application(
    modules=[
        Commands(),
        Tests()
    ]
)
```

```sh
$ logos
usage: logos [--app-url APP_URL] {test} ...
logos: error: the following arguments are required: command

$ logos test --help
usage: logos test [-h] [--name NAME]

options:
  -h, --help   show this help message and exit
  --name NAME

$ logos test
Hello Anonymous

$ logo test --name=foo
Hello foo
```

## Core Concepts

LogosCDI is built around the concepts of Resources and References, which allow for a flexible and powerful dependency injection system.

### Resources

Resources are the objects that are managed by the dependency injection container. There are three main types of resources:

#### `Parameter`

A `Parameter` is the simplest type of resource. It holds a static value, which can be a string, an integer, a list, a dictionary, or any other Python object. Parameters can also contain nested `Reference` objects, which will be resolved by the container.

**Example:**

```python
from logos_cdi.resource import Parameter
from logos_cdi.reference import Reference

# A simple parameter
db_host = Parameter("localhost")

# A parameter with a nested reference
db_config = Parameter({
    "host": Reference("db_host"),
    "port": 5432
})
```

#### `Service`

A `Service` resource represents a class instance. The container will automatically instantiate the class and inject its dependencies. Dependencies are defined as a dictionary of `parameters`, where the keys are the argument names in the class's `__init__` method.

**Example:**

```python
from logos_cdi.resource import Service
from logos_cdi.reference import Reference

class DatabaseConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port

# Define a service for the DatabaseConnector
database_service = Service(
    class_path="my_module.DatabaseConnector",
    parameters={
        "host": Reference("db_host"),
        "port": Reference("db_port")
    }
)
```

#### `Singleton`

A `Singleton` is similar to a `Service`, but the container will only create a single instance of the class within a given context. Every time the singleton is requested from the container, the same instance will be returned.

**Example:**

```python
from logos_cdi.resource import Singleton

# A singleton logger service
logger_service = Singleton(
    class_path="my_module.Logger",
    parameters={}
)
```

### References

References are used to link resources together. They act as pointers to other resources in the container.

#### `Reference`

The standard `Reference` is used to get another resource from the container by its name.

**Example:**
`db_host = Reference("database_host_parameter")`

#### `Parent`

A `Parent` reference is used to get a resource from a parent context. This is useful when you have nested contexts.

**Example:**
`global_config = Parent("config_from_parent_context")`

#### `Context`

A `Context` reference allows you to inject the context object itself as a dependency.

**Example:**
`current_context = Context()`

#### `AllRegisteredReference`

This reference is used to get all resources that have been registered with a specific `Registry`. It returns a dictionary where the keys are the names of the resources and the values are the resolved resources.

**Example:**
```python
# Get all commands from the command registry
all_commands = AllRegisteredReference("commands.registry")
```

