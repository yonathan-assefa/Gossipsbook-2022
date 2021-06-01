from rest_framework.authtoken.models import Token
from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate
import json
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


def get_token(request):
    # data_json = json.loads(request.body)
    # username = data_json["username"]
    # password = data_json["password"]
    # user = authenticate(username=username, password=password)
    # if user:
    #     user_t = User.objects.get(username=username)
    #     token = Token.objects.create(user=user_t)
    #     dictio = {
    #         "token": token,
    #         "user": user_t
    #     }
    username = request.GET.get("u")
    password = request.GET.get("pw")
    print(username, password)
    if username and password:
        user = authenticate(username=username, password=password)
        print("Here  ")
        if user:
            user_obj = User.objects.get(username=username)
            token = Token.objects.get(user=user_obj)
            dictio = {
                'token': str(token),
            }
            return JsonResponse(dictio, safe=False)
        raise PermissionDenied()

        print("username")
        return JsonResponse("Hello", safe=False)
    raise Http404("Please Provide Both Username and Password...")

    # raise Http404