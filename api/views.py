'''Views for API'''
from . import serializers, models
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.settings import api_settings
from rest_framework.generics import get_object_or_404



class SuperUserPermission(permissions.BasePermission):
    '''Permissions for super user'''
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        elif request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
    

class ExecutivePermission(permissions.BasePermission):
    '''Permissions for executive user'''
    
    def has_permission(self, request, view):
        if request.user.is_executive:
            return True

        elif request.user.is_authenticated:
            # Allow authenticated users to have detailed GET method access
            return request.method == 'GET' or request.method in permissions.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
         if request.user.is_executive:
            return True
         elif request.user.is_authenticated and request.method == 'GET':
             return True
         return False
    

class CreateUserView(generics.CreateAPIView):
    '''Create a New User view'''
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


    def create(self, request, *args, **kwargs):
        '''Create user'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({'message': 'User created successfullly'}, status=status.HTTP_201_CREATED)
    

class CreateTokenView(TokenObtainPairView):
    '''Create a new auth token for user'''
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''manage authenticated user'''
    serializer_class = serializers.UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [SuperUserPermission]


    def get_object(self):
        '''Retrieve and return the authenticated user'''
        return self.request.user
    

class BaseModelViewSet(viewsets.ModelViewSet):
    '''Base viewset for managing common API functionality'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [ExecutivePermission]

    def perform_create(self, serializer):
        '''create a new instance of the model'''
        serializer.save(user=self.request.user)


class ManufacturerViewSet(BaseModelViewSet):
    '''view for managing manufacturer API'''
    serializer_class = serializers.ManufacturerSerializer
    queryset = models.Manufacturer.objects.all()
        

class BrandViewSet(BaseModelViewSet):
    '''view for managing Brand API'''
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()


class CategoryViewSet(BaseModelViewSet):
    '''view for managing Category API'''
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class ProductViewSet(BaseModelViewSet):
    '''view for managing Product API'''
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()


class VariantViewSet(BaseModelViewSet):
    '''view for managing Variant API'''
    serializer_class = serializers.VariantSerializer
    queryset = models.Variant.objects.all()

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def create(self, request, *args, **kwargs):
    #     '''Create multiple variants for the product'''
    #     product_id = self.kwargs.get('product_id')
    #     product = get_object_or_404(models.Product, id=product_id)
        
    #     # Extract variant data from request data
    #     variants_data = request.data if isinstance(request.data, list) else [request.data]

    #     # Validate and create each variant associated with the product
    #     for variant_data in variants_data:
    #         serializer = self.get_serializer(data=variant_data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(product=product)

    #     return Response({'message': 'Variants created successfully'}, status=status.HTTP_201_CREATED)
