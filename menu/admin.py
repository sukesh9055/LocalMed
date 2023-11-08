from django.contrib import admin
from .models import Category, Medicine_lobby
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name','vendor__vendor_name')

class MedicineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Medicine_title',)}
    list_display = ('Medicine_title', 'category','price','is_available','vendor', 'updated_at')
    search_fields = ('Medicine_title','category__category_name','vendor__vendor_name','price')
    list_filter = ('is_available',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Medicine_lobby,MedicineAdmin)