from django.urls import path
from . import views
from .views import PatchListView

app_name = 'patch_list'

urlpatterns = [
    path('', views.index, name='index'),
    path('list', PatchListView.as_view(), name='list'),
]