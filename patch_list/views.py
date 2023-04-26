from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.
import os
# csv ダウンロード用
import csv
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime

from .models import (
    Patchs, Patchs_file
)


def index(request):
    return render(request, 'index.html')

class PatchListView(ListView):
    # modelで作成したclassを指定
    model = Patchs
    template_name = 'patch/patch_list.html'

    def get_queryset(self):
        query = super().get_queryset()
        # URLに記載した名前
        name = self.request.GET.get('application_name', None)
        if name:
            query = query.filter(
                name=name
            )
        return query

    # csvダウンロード用追加した
    # テンプレートに渡すコンテキストデータを返すメソッド
    # ListView クラスのget_context_data メソッドを利用
    def get_context_data(self, **kwargs):
        # クラスのget_context_dataメソッドを呼び出し、コンテキストデータを取得
        context = super().get_context_data(**kwargs)
        print(f"1st{context}")
        # GETパラメーターにapplication_nameが含まれている場合に、CSVファイルのダウンロードURLをコンテキストに追加
        if 'application_name' in self.request.GET:
            print("2nd", self.request.GET)
            print("2nd type", type(self.request.GET))
            # reverse('patch_list:list')で、patch_listという名前のURLパターンのURLを取得
            # self.request.GET.urlencode()で、GETパラメーターをエンコードした文字列を取得
            context['csv_url'] = reverse('patch_list:list') + '?' + self.request.GET.urlencode()
            # context['csv_url']に、CSVファイルのダウンロードURLを追加
            context['csv_url'] += '&export=csv'
            print("if context", context)
        print("final", context)
        return context



    def create_csv_response(self, queryset):
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="search_results_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Patch Name', 'Patch No', 'Release Date'])
        for patch in queryset:
            writer.writerow([patch.name, patch.patch_name, patch.patch_no, patch.release_date])
        return response

    def get(self, request, *args, **kwargs):
        if 'export' in request.GET and request.GET['export'] == 'csv':
            queryset = self.get_queryset()
            response = self.create_csv_response(queryset)
            return response
        else:
            return super().get(request, *args, **kwargs)





# TODO: ダウンロード出来ない ------------------------------------------------------ #
    # 以下例だと出来るけど、urlを開いた瞬間にすぐにダウンロードしてしまう。

    # def get(self, request, *args, **kwargs):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="patch.csv"'
    #
    #     writer = csv.writer(response)
    #     writer.writerow(['id', 'name', 'release_date'])
    #
    #     for patch in self.get_queryset():
    #         writer.writerow([patch.id, patch.name, patch.release_date])
    #
    #     return response

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(f"test:{self.template_name}")
    #     if 'application_name' in self.request.GET:
    #         response = HttpResponse(content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    #         writer = csv.writer(response)
    #         writer.writerow(['Name', 'Patch Name', 'Patch No', 'Release Date'])
    #         for patch in context['object_list']:
    #             writer.writerow([patch.name, patch.patch_name, patch.patch_no, patch.release_date])
    #         context['csv_url'] = reverse('patch_list:list') + '?' + self.request.GET.urlencode()
    #         context['csv_url'] += '&export=csv'
    #         context['csv_link'] = response
    #     return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if 'application_name' in self.request.GET:
    #         response = HttpResponse(content_type='text/csv')
    #         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #         response['Content-Disposition'] = f'attachment; filename="search_results_{timestamp}.csv"'
    #         writer = csv.writer(response)
    #         writer.writerow(['Name', 'Patch Name', 'Patch No', 'Release Date'])
    #         for patch in context['object_list']:
    #             writer.writerow([patch.name, patch.patch_name, patch.patch_no, patch.release_date])
    #         context['csv_url'] = reverse('patch_list:list') + '?' + self.request.GET.urlencode()
    #         context['csv_url'] += '&export=csv'
    #         context['csv_link'] = response
    #     return context