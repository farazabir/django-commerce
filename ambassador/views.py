import math
import random
import string
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from administrator.serializers import LinkSerializer, ProductSerializer
from common.authentication import JwtAuthenticationCookie
from core.models import Link, Order, Product, User
import time
from django_redis import get_redis_connection


class ProductFrontendAPIView(APIView):
    @method_decorator(cache_page(60*60*2), name='prodcuts_frontend')
    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductBackendAPIView(APIView):
    def get(self, request):
        products = cache.get('products_backend')
        if not products:
            time.sleep(2)
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60*60)

        s = request.query_params.get('s', '')
        if s:
            products = list([
                p for p in products
                if (s.lower() in p.title.lower() or s.lower() in p.description.lower())
            ])

        total = len(products)

        sort = request.query_params.get('sort', None)
        if sort == 'asc':
            products.sort(key=lambda p: p.price)
        elif sort == 'desc':
            products.sort(key=lambda p: p.price, reverse=True)

        per_page = 9
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page*per_page
        data = ProductSerializer(products[start:end], many=True).data
        return Response({
            'data': data,
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total/per_page)
            }
        })


class LinkAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = LinkSerializer(data={
            'user': user.id,
            'code': ''.join(random.choices(string.ascii_lowercase+string.digits, k=6)),
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StatsAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        links = Link.objects.filter(user_id=user.id)

        return Response([self.format(link)for link in links])

    def format(self, link):
        orders = Order.objects.filter(code=link.code, complete=1)

        return {
            'code': link.code,
            'count': len(orders),
            'revenue': sum(o.ambassador_revenue for o in orders)
        }


class RankingAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        con = get_redis_connection("default")
        rankings = con.zrevrangebyscore(
            'rankings', min=0, max=9999, withscores=True)
        return Response({
            r[0].decode('utf-8'): r[1] for r in rankings
        })
