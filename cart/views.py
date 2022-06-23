from itertools import product
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import OrderItem, User, Cart, DeliveryCost
from .serializers import UserSerializer, CartSerializer, DeliveryCostSerializer, OrderItemSerializer
from products.models import Product
# from .helpers import CartHelper


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('id')
    serializer_class = OrderItemSerializer

    @action(methods=['post', 'put'], detail=True)
    def add_to_cart(self, request, pk=None):
        """Add an item to a user's cart.
        Adding to cart is disallowed if there is not enough inventory for the
        product available. If there is, the quantity is increased on an existing
        cart item or a new cart item is created with that quantity and added
        to the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        # Disallow adding to cart if available inventory is not enough
        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print ("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = OrderItem.objects.filter(cart=cart,product=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = OrderItem(cart=cart, product=product, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(methods=['post', 'put'], detail= True)
    def remove_from_cart(self, request, pk=None):
        """Remove an item from a user's cart.
        Like on the Everlane website, customers can only remove items from the
        cart 1 at a time, so the quantity of the product to remove from the cart
        will always be 1. If the quantity of the product to remove from the cart
        is 1, delete the cart item. If the quantity is more than 1, decrease
        the quantity of the cart item, but leave it in the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        try:
            cart_item = OrderItem.objects.get(cart=cart,product=product)
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)



    # @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    # def checkout(self, request, *args, **kwargs):

    #     try:
    #         user = User.objects.get(pk=int(kwargs.get('userId')))
    #     except Exception as e:
    #         return Response(status=status.HTTP_404_NOT_FOUND,
    #                         data={'Error': str(e)})

        # cart_helper = CartHelper(user)
        # checkout_details = cart_helper.prepare_cart_for_checkout()

        # if not checkout_details:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={'error': 'Cart of user is empty.'})

        # return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})


class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer