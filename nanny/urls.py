from django.urls import path

from . import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from .models import Host,Nanny,Schedule
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, viewsets, routers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
class FullHostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('url','username','phone','location','kids','password')
class SafeHostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('id','username','phone','location','kids')
class NannySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nanny
        fields = ('username','phone','location','price','password')
class SafeNannySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nanny
        fields = ('username','phone','location','price')
class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ('host','nanny','time','payment')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = SafeHostSerializer

class NannyViewSet(viewsets.ModelViewSet):
    queryset = Nanny.objects.all()
    serializer_class=SafeNannySerializer
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class=ScheduleSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hosts',HostViewSet)
router.register(r'nannys',NannyViewSet)
router.register(r'schedules',ScheduleViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.index, name='index'),
    path('parentSignUp', views.parentSignUp, name='parentSignUp'),
    path('parentProcess', views.parentProcess, name = 'parentProcess'),
    path('nannySignUp', views.nannySignUp, name = 'nannySignUp'),
    path('nannyProcess', views.nannyProcess, name = 'nannyProcess'),
    path('nanny/done', views.done, name = 'done'),
    path('nanny/locator', views.locator, name = 'locator')
]
