from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.
import os
# csv ダウンロード用
import csv
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime

# excelダウンロード用
import openpyxl

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
        checks = self.request.GET.get('patch_check', None)

        start_month = self.request.GET.get('start_date', None)
        end_month = self.request.GET.get('end_date', None)

        if name:
            query = query.filter(
                name=name
            )

        if checks:
            query = query.filter(
                checks=checks
            )

        if start_month and end_month:
            start_month = datetime.strptime(start_month, '%Y-%m')
            end_month = datetime.strptime(end_month, '%Y-%m')
            query = query.filter(release_date__range=(start_month, end_month))

        return query

    # csvダウンロード用追加した
    # テンプレートに渡すコンテキストデータを返すメソッド
    # ListView クラスのget_context_data メソッドを利用
    def get_context_data(self, **kwargs):
        # クラスのget_context_dataメソッドを呼び出し、コンテキストデータを取得
        context = super().get_context_data(**kwargs)

        # GETパラメーターにapplication_nameが含まれている場合に、CSVファイルのダウンロードURLをコンテキストに追加
        # ここで指定するのはhtmlで記載された番号をしていする
        if 'application_name' or 'patch_check' or 'start_date' or 'end_date' in self.request.GET:
            # reverse('patch_list:list')で、patch_listという名前のURLパターンのURLを取得
            # self.request.GET.urlencode()で、GETパラメーターをエンコードした文字列を取得
            context['excel_url'] = reverse('patch_list:list') + '?' + self.request.GET.urlencode()
            # context['csv_url']に、CSVファイルのダウンロードURLを追加
            context['excel_url'] += '&export=excel'
        return context



    # def create_csv_response(self, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #     response['Content-Disposition'] = f'attachment; filename="search_results_{timestamp}.csv"'
    #     writer = csv.writer(response)
    #     writer.writerow(['Name', 'Patch Name', 'Patch No', 'Release Date', 'Patch Name'])
    #     for patch in queryset:
    #         writer.writerow([patch.name, patch.patch_name, patch.patch_no, patch.release_date])
    #     return response

    def create_excel_response(self,queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="search_results_{timestamp}.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        worksheet['A1'] = 'Name'
        worksheet['B1'] = 'Patch Name'
        worksheet['C1'] = 'Patch No'
        worksheet['D1'] = 'Release Date'
        worksheet['E1'] = 'Content'

        row_num = 2
        for patch in queryset:
            worksheet.cell(row=row_num, column=1, value=patch.name)
            worksheet.cell(row=row_num, column=2, value=patch.patch_name)
            worksheet.cell(row=row_num, column=3, value=patch.patch_no)
            worksheet.cell(row=row_num, column=4, value=patch.release_date)
            # worksheet.cell(row=row_num, column=5, value=patch.content)
            row_num += 1

        workbook.save(response)

        return response


    def get(self, request, *args, **kwargs):
        if 'export' in request.GET and request.GET['export'] == 'excel':
            queryset = self.get_queryset()
            response = self.create_excel_response(queryset)
            return response
        else:
            return super().get(request, *args, **kwargs)
