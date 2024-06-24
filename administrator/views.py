from django.core.cache import caches
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from administrator.serializers import LinkSerializer, OrderSerializer, ProductSerializer
from common.authentication import JwtAuthenticationCookie
from common.serializers import UserSerializer
from core.models import Link, Order, Product, User

# Create your views here.


class AmbassadorAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        serializer = UserSerializer(ambassadors, many=True)
        return Response(serializer.data)


class ProductGenericAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        return self.list(request)

    def post(self, request):
        response = self.create(request)
        for key in caches.keys('*'):
            if 'products_frontend' in key:
                caches.delete(key)
            caches.delete('products_backend')
        return response

    def put(self, request, pk=None):

        respone = self.partial_update(request, pk)
        for key in caches.keys('*'):
            if 'products_frontend' in key:
                caches.delete(key)
            caches.delete('products_backend')
        return respone

    def delete(self, request, pk=None):
        response = self.destroy(request, pk)

        for key in caches.keys('*'):
            if 'products_frontend' in key:
                caches.delete(key)
            caches.delete('products_backend')
        return response


class LinkApiView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)


class OrderAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(complete=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
