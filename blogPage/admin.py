from django.contrib import admin
from .models import BlogComment, BlogItem
# Register your models here.
admin.site.register(BlogComment)
admin.site.register(BlogItem)