'''URL mappings for API'''
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('manufacturer', views.ManufacturerViewSet)
router.register('brand', views.BrandViewSet)
# router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('variant', views.VariantViewSet)



urlpatterns = [
    path('user/create/', views.CreateUserView.as_view(), name='create-user'),
    path('user/me/', views.ManageUserView.as_view(), name='manage-user'),
    path('', include(router.urls)),
]