from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListCreateAPIView,DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import HostCategory,Host
from .serializers import HostModelSerializers,HostCategoryModelSeiralizer


class HostCategoryListAPIView(ListCreateAPIView):
    queryset = HostCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id").all()
    serializer_class = HostCategoryModelSeiralizer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

class HostModelViewSet(ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostModelSerializers
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]