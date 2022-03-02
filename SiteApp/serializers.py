from rest_framework import serializers
from .models import User, Product
from django.contrib.auth import authenticate

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=128, min_length=4)
    # token = serializers.CharField(max_length=256)

    class Meta:
        model = User
        fields = ['id', 'username',]

class RegistrationSerializer(serializers.ModelSerializer):
    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'user_id' : user.pk,
            'token': user.token,
            'username' : user.username
        }



class PasswordRecoverySerializer(serializers.Serializer):
    username = serializers.IntegerField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username',)



class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    image = serializers.CharField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    code = serializers.CharField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price')

    def create(self, validated_data):
        return Product.objects.create(**validated_data)