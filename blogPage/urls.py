from django.urls import path
from .views import Blogs,SpecificBlog,CreateBlog,deleteComment,deleteBlog

urlpatterns = [
    path('blogs/',Blogs.as_view(),name='blogs'),
    path('blog/<str:blog_id>/',SpecificBlog.as_view(),name="blog"),
    path('create-blog/',CreateBlog.as_view(),name='create_blog'),
    path('delete-comment/',deleteComment),
    path('delete-blog/',deleteBlog),
]
