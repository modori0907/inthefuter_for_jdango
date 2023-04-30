from django.urls import path
from . import views
from .views import PatchListView, patch_create, patch_update, patch_delete

app_name = 'patch_list'

urlpatterns = [
    # path('', views.index, name='index'),
    path('list', PatchListView.as_view(), name='list'),
    # 追加する為のurlpattern
    path('create/', patch_create, name='create'),
    # 更新する為のurlpattern
    path('update/<int:pk>/', patch_update, name='update'),

    # 削除する為のurlpattern
    path('delete/<int:pk>/', patch_delete, name='delete'),
    # 詳細画面を表示するための処理
    path('detail/<int:pk>/', views.PatchDetailView.as_view(), name='detail'),



]