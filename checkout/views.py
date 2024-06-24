from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from checkout.serializers import LinkSerializer
from core.models import Link

# Create your views here.


class LinkAPIView(APIView):
    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)
