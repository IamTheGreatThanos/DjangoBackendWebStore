from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Product
from django.http import *
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, ProductSerializer, PasswordRecoverySerializer
from rest_framework import generics

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordRecoveryAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordRecoverySerializer

    def post(self, request):
        user = User.objects.filter(username=request.data.get('username'))
        serializers = PasswordRecoverySerializer(user, many=False)

        return Response({'password' : '123'})


class ListUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many = True)

        return Response({'users' : serializers.data})


class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)

        except ValueError as error:
            Response(error.args[0], status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status.HTTP_200_OK)

        except ValueError as error:
            Response(error.args[0], status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            id = request.data.get('id')
            product = Product.objects.get(id=id)
            product.delete()
            return Response({'status' : 'Product is deleted successfully.'})

        except ValueError as error:
            Response(error.args[0], status.HTTP_404_NOT_FOUND)


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ValueError as error:
            Response(error.args[0], status.HTTP_404_NOT_FOUND)


class ProductsGetTopsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = Product.objects.all().order_by('rating').reverse()[:4]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ValueError as error:
            Response(error.args[0], status.HTTP_404_NOT_FOUND)


