from django.contrib import admin
# csvデータをインポート出来るようにする
from import_export.admin import ImportExportModelAdmin

from .models import (
    Patchs, Patchs_file
)

@admin.register(Patchs)
class PatchAdmin(ImportExportModelAdmin):
    pass

# Register your models here.

# admin.site.register(Patchs)

# csvデータをインポート出来るようにするため

