from django.db import models

# Create your models here.

# class ApplicationNames(models.Model):
#     name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'application_names'
#     # 管理画面でわかりやすく表示するため
#     def __str__(self):
#         return self.name

class Patchs(models.Model):
    name = models.CharField(max_length=100)
    checks = models.CharField(max_length=100)
    release_date = models.DateField()
    patch_name = models.CharField(max_length=100)
    patch_no = models.CharField(max_length=100)
    reference_url = models.URLField()
    # 更新した日時を画面上に表示させるため
    # updated_at = models.DateTimeField(auto_now=True)

    # 検索範囲を指定するため
    @property
    def release_month(self):
        return self.release_date.strftime('%Y-%m')



#　後で追加していく
    class Meta:
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

