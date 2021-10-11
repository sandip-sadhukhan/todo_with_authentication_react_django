from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer, UserLoginSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate


class GetUserView(APIView):
    permission_classes = (IsAuthenticated,)
    """
    It will take token and return the user's name, email, phone
    """

    def get(self, request):
        data = {
            'email': request.user.email,
            'name': request.user.name,
            'phone': request.user.phone
        }
        return Response(data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LoginView(APIView):
    """
    It will check if the email/phone and password matches for some user
    if match then return Token otherwise return Error
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.data['identifier']
            password = serializer.data['password']
            user = authenticate(email=identifier, password=password)
            token = None
            if user is not None:
                token = Token.objects.get_or_create(user=user)[0]
                # print(token.key)
            else:
                # check with phone
                user = User.objects.filter(phone=identifier)
                if user.count() > 0:
                    user_email = user[0].email
                    # print(user)
                    user = authenticate(email=user_email, password=password)
                    if user is not None:
                        token = Token.objects.get_or_create(user=user)[0]
                        # print(token.key)
                    else:
                        return Response(data={'success': False, 'msg': 'Wrong Credentials.'})
                else:
                    return Response(data={'success': False, 'msg': 'Wrong Credentials.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data={'success': True, 'token': token.key}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
