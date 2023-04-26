from django.contrib import admin
from .models import (
    Patchs, Patchs_file
)
# Register your models here.

admin.site.register (
    [Patchs, Patchs_file]
)