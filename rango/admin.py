from django.contrib import admin
from rango.models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display=('title', 'category', 'url')

admin.site.register(Page, PageAdmin)

<<<<<<< HEAD
admin.site.register(UserProfile)
=======
>>>>>>> 00ce1efe6b75c907b9127012b28d62cf4445a70c
