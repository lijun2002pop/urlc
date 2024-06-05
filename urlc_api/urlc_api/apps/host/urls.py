from django.http import HttpResponse
from django.urls import path, re_path
from .views import HostModelViewSet,HostCategoryListAPIView

def aa(request):
    return HttpResponse('ok')
urlpatterns = [
    path('category',HostCategoryListAPIView.as_view()),
    re_path('(?P<pk>\d+)', HostModelViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    re_path(r'', HostModelViewSet.as_view({'get': 'list','post': 'create'})),

    # re_path(r'^(?P<pk>\d+)/$', HostModelViewSet.as_view({'get': 'retrieve','delete': 'destroy'}))
]