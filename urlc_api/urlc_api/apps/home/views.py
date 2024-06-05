import json
import mimetypes
import os
import re
import time
from wsgiref.util import FileWrapper

from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
def home(request):
    return HttpResponse('hello')


class Test(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        time.sleep(0.5)
        return Response({'msg': 'hello li'})


class Music_worlds(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        name = request.GET.get('name')
        with open(f'files//{name}.lrc', 'r', encoding='utf-8')as f:
            words = f.read()
        return Response({'msg': 'ok', 'words': words})


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

def play(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    name = request.GET.get('name')
    path = f'files//{name}.mp3'
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

class Music_list(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        li = []
        for i in os.listdir('files'):
            if i.split('.')[0] not in li:
                li.append(i.split('.')[0])
        return JsonResponse(li,safe=False)