from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import User

class Login(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email_value = serializer.data.get("email")
            user = User.objects.get(email=email_value)


            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': "serialized_user", 'token': "token"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)