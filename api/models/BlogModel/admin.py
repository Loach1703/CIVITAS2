from django.contrib import admin
from .models import Blog
# Register your models here.
class blogdisplay(admin.ModelAdmin):
    list_display = ('text_blog',)

admin.site.register(Blog,blogdisplay)