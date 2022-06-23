from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'delivery-cost', views.DeliveryCostViewSet)
router.register(r'OrderItem', views.OrderItemViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include((router.urls, 'cart'))),
]