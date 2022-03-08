from django.http import HttpResponse, JsonResponse

from starter.schema import User
from zark.views.base import APIView


class Test(APIView):
    schema = User

    def post(self, request, *args, **kwargs):
        print(self.schema.instance)
        return JsonResponse(self.schema.instance())
