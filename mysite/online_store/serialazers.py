from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password','first_name','last_name','age',
                  'phone_number','date_registred','status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerialazer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerialazer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']


class CategorySerialazer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductlistSerialazer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='%d:%m:%Y')

    class Meta:
        model = Product
        fields = ['product_name','price','date_created','id','category']


class ProductPhotoSerialazer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['image']


class ReviewSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RaitingsSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Raitings
        fields = '__all__'


class ProductSerialazer(serializers.ModelSerializer):
    category = CategorySerialazer()
    raitings = RaitingsSerialazer(read_only=True,many=True)
    review = ReviewSerialazer(read_only=True,many=True)
    product = ProductPhotoSerialazer(read_only=True,many=True)
    date_created = serializers.DateTimeField(format='%d-%m-%Y')
    average_raitings = serializers.SerializerMethodField()
    owner = UserProfileSimpleSerialazer()

    class Meta:
        model = Product
        fields = ['id','product_name','category','description','product','video','price','have',
                  'raitings','review','date_created','average_raitings','owner']

    def get_average_raitings(self,obj):
        return obj.get_average_raitings()


class CartItemSerialazer(serializers.ModelSerializer):
    product = ProductlistSerialazer(many=True,read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),write_only=True,source='product')

    class Meta:
        model = CarItem
        fields = ['id','product','product_id','quantity','get_total_price']


class CartSerialazer(serializers.ModelSerializer):
    items = CartItemSerialazer(read_only=True,many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','user','items','total_price']

        def get_total_price(self,obj):
            return obj.get_total_price()






