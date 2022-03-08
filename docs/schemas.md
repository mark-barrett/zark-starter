# Schemas
Schemas in Zark are Pydantic based classes with added features. A Schema's purpose in Zark is
to dictate a bodies content when requesting or responding from a View.

As they are Pydantic based, anything you can do with Pydantic Models, you can do with Schemas.

Schemas solve two core issues:

- Providing Validations for API Views
- Provide a way to convert a request payload into a Python object and then back to the same format for the response

Schemas tie really nicely in with Views. See the following example.

#### Define the Schema (Based on Pydantic Models)
```python
from typing import Optional
from zark.schemas.base import JSONSchema

class User(JSONSchema):
    first_name: str
    last_name: str
    email: str
    age: Optional[int]
```

#### Define the View (Based on Django Views)
```python
from django.http import HttpResponse
from starter.schema import User
from zark.views.base import APIView

class CreateUser(APIView):
    schema = User

    def get(self, request, *args, **kwargs):
        return HttpResponse(f"Welcome {self.schema.instance.first_name}!")
```

When a request for that View, the request body is applied to the schema defined in the Create User View.

If the Validation fails, errors are returned in a nice format (supporting errors from Pydantic), if the validation
passes, then the Instance of the schema is now available in the instance attribute of the schema.

## Schema Types
The fun doesn't stop at JSON. We included XML support (for those who want it), where the XML will be validated against the
Pydantic model and like above, stored as an instance.

Have some other format you want to support like YAML? It's pretty easy to extend with your Schema type. All you have to
do is extend the base Schema and implement a constructor and deserializer.
