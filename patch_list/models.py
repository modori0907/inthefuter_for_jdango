from django.db import models
#掲示板でtimezoneを使うため
from django.utils import timezone

class Patchs(models.Model):
    name = models.CharField(max_length=100)
    # help_textで各項目に補足を追記できる
    checks = models.CharField(max_length=100,help_text='チェック有無')
    release_date = models.DateField()
    patch_name = models.CharField(max_length=100)
    patch_no = models.CharField(max_length=100)
    reference_url = models.URLField()
    # 更新した日時を画面上に表示させるため
    updated_at = models.DateTimeField(auto_now=True)
    # チェック項目
    impact_check = models.BooleanField(default=False)
    # 新規作成した日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 閲覧した回数を記録
    views_count = models.IntegerField(default=0)

    # 内容追加
    #  blank=Trueで入力無しを許可する
    Remark = models.TextField(max_length=10000, blank=True)
    Notes = models.TextField(max_length=10000, blank=True)

    # 検索範囲を指定するため
    @property
    def release_month(self):
        return self.release_date.strftime('%Y-%m')



#　後で追加していく
    class Meta:
        # ListViewで表示したときに、更新した降順に表示させるために
        ordering = ['-updated_at']
        db_table = "patchlists"

    def __str__(self):
        return self.name

class Patchs_file(models.Model):
    patch_file = models.FileField()
    patch_name = models.ForeignKey(
        Patchs, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "patch_file"



    def __str__(self):
        return self.patch_name.patch_name

# コメント追加用
class Comment(models.Model):
    patchs = models.ForeignKey(Patchs, on_delete=models.CASCADE, related_query_name='comments')
    author = models.CharField(default="anonymous", max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_date']

