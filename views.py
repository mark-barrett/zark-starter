import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from pydantic import ValidationError

from starter.schema import User


class ZarkView(View):

    schema = None

    @classmethod
    def as_view(cls, **initkwargs):
        # todo: validators to check there is a schema if needed. e.g. don't need a schema for the GET?
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    "The method name %s is not accepted as a keyword argument "
                    "to %s()." % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. as_view "
                    "only accepts arguments that are already "
                    "attributes of the class." % (cls.__name__, key)
                )

        def view(request, *args, **kwargs):
            # todo: check content type etc.
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            request_body = json.loads(request.body.decode('utf-8'))
            # todo: get all exceptions. Do proper exception handling. this is just a test
            try:
                _ = self.schema(**request_body)
                if not hasattr(self, "request"):
                    raise AttributeError(
                        "%s instance has no 'request' attribute. Did you override "
                        "setup() and forget to call super()?" % cls.__name__
                    )
                return self.dispatch(request, *args, **kwargs)
            except ValidationError as exception:
                errors = {}
                for error in exception.args[0]:
                    errors[error._loc] = [
                        error.exc.msg_template
                    ]
                # todo: handle all error wrapper types to make it easier to understand whats wrong
                return JsonResponse({
                    'errors': errors
                })

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        return view


class Test(ZarkView):

    schema = User

    def post(self, request, *args, **kwargs):
        return HttpResponse('OK')
