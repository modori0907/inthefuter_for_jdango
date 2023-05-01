from datetime import datetime

# excelダウンロード用
import openpyxl
# Create your views here.
# csv ダウンロード用
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
# 詳細画面を表示するため
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# 登録画面を作成するため
from .forms import PatchForm, CommentForm
from .models import (
    Patchs, Comment
)


# def index(request):
#     return render(request, 'index.html')

# パッチリストを作成する為の処理
def patch_create(request):
    if request.method == 'POST':
        form = PatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patch_list:list')

    else:
        form = PatchForm()
    return render(request, 'patch/patch_create.html', {'form': form})


# パッチリストを更新する為の処理
def patch_update(request, pk):
    patch = Patchs.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatchForm(request.POST, instance=patch)
        if form.is_valid():
            form.save()
            return redirect('patch_list:list')
    else:
        form = PatchForm(instance=patch)
    return render(request, 'patch/patch_update.html', {'form': form})


# パッチリストを削除する処理
def patch_delete(request, pk):
    patch = Patchs.objects.get(pk=pk)
    patch.delete()
    return redirect('patch_list:list')


# パッチリストの詳細画面を表示する
# コメント登録機能を追加
# class PatchDetailView(DetailView):
#
#     model = Patchs
#     template_name = 'patch/patch_detail.html'


# def PatchDetailView(request, pk):
#     patch_list = get_object_or_404(Patchs, pk=pk)
#     comments = patch_list.comments.filter(active=True)
#
#     # フォームの送信がPOSTメソッドで行われた場合、フォームのバリデーションが成功した場合に、
#     # 新しいコメントを作成
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.patchs = patch_list
#             comment.save()
#             return redirect('patch_list:detail', pk = patch_list.pk)
#     else:
#         form = CommentForm()
#
#     return render(request, 'patch/patch_detail.html', {'patch_list':patch_list, 'comment': comments, 'form': form})

class PatchDetailView(DetailView):
    model = Patchs
    template_name = 'patch/patch_detail.html'
    context_object_name = 'patch_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(patchs=self.get_object())
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.patchs = self.object
            comment.save()
            return redirect('patch_list:detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class PatchListView(ListView):
    # modelで作成したclassを指定
    model = Patchs
    template_name = 'patch/patch_list.html'

    # 検索画面の結果を表示させるため。getで取得した値
    def get_queryset(self):
        query = super().get_queryset()
        # URLに記載した名前
        name = self.request.GET.get('application_name', None)
        # checks = self.request.GET.get('patch_check', None)
        impact_check = self.request.GET.get('impact_check', None)

        start_month = self.request.GET.get('start_date', None)
        end_month = self.request.GET.get('end_date', None)

        if name:
            query = query.filter(
                name=name
            )

        if impact_check:
            query = query.filter(
                impact_check=impact_check
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
        if 'application_name' or 'impact_check' or 'start_date' or 'end_date' in self.request.GET:
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

    # エクセス記載処理
    def create_excel_response(self, queryset):
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
