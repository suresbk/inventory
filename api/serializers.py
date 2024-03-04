'''Serilizers for API views'''

from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):
    '''Serializer for User object'''

    class Meta:
        model = get_user_model()
        fields = ['mobile', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        '''Create and return a User with Encrypted password'''
        return get_user_model().objects.create_user(**validated_data)
    

    def update(self, instance, validated_data):
        '''Update and return user'''
        password = validated_data.pop('password', None)
        user  = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for the user auth token'''
    mobile = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        '''validate and authenticate the user'''
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=mobile,
            password=password,
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authorization')
        
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs.pop('password', None)
        return attrs
    

class ManufacturerSerializer(serializers.ModelSerializer):
    '''serializer for manufacturer'''

    class Meta:
        model = models.Manufacturer
        fields = ['id', 'name', 'date_added']
        read_only_fields = ['id', 'date_added']


class BrandSerializer(serializers.ModelSerializer):
    '''serializer for brand'''

    class Meta:
        model = models.Brand
        fields = ['id', 'name', 'date_added', 'manufacturer']
        read_only_fields = ['id', 'date_added']


class CategorySerializer(serializers.ModelSerializer):
    '''serializer for category'''

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'date_added', 'parent_category']
        read_only_fields = ['id', 'date_added']


class VariantSerializer(serializers.ModelSerializer):
    '''serializer for variant'''

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(VariantSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
       model = models.Variant
       fields = ['id', 'name', 'date_added', 'price', 'SKU', 'stock', 'description', 'manufacturer', 'brand', 'product']
       read_only_fields = ['id', 'date_added']


class ProductSerializer(serializers.ModelSerializer):
    '''serializer for product'''

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'date_added', 'manufacturer', 'brand', 'description']
        read_only_fields = ['id', 'date_added']

    # def create(self, validated_data):
    #     product = models.Product.objects.create(**validated_data)
    #     models.Variant.objects.create(product=product)
    #     return product


# class VariantSerializer(serializers.ModelSerializer):
#     '''serializer for variant'''

#     product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), required=False)

#     class Meta:
#         model = models.Variant
#         fields = ['id', 'name', 'date_added', 'price', 'SKU', 'stock', 'description', 'product']
#         read_only_fields = ['id', 'date_added']

# class ProductSerializer(serializers.ModelSerializer):
#     '''serializer for product'''

#     variants = VariantSerializer(many=True, required=False)

#     class Meta:
#         model = models.Product
#         fields = ['id', 'name', 'date_added', 'manufacturer', 'brand', 'description', 'variants']
#         read_only_fields = ['id', 'date_added']

#     def create(self, validated_data):
#         variants_data = validated_data.pop('variants', [])
#         product = models.Product.objects.create(**validated_data)

#         manufacturer = validated_data.get('manufacturer')
#         brand = validated_data.get('brand')
#         user = self.context['request'].user

#         for variant_data in variants_data:
#             variant_data['manufacturer'] = manufacturer
#             variant_data['brand'] = brand
#             variant_data['user'] = user
#             if 'product' not in variant_data:
#                 variant_data['product'] = product
#             models.Variant.objects.create(**variant_data)
#         return product


