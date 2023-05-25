
from urllib import request
from django.shortcuts import redirect, render,HttpResponseRedirect,HttpResponse
from django.views.generic import ListView,DetailView,CreateView,FormView
from .models import BlogItem,BlogComment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse_lazy





class Blogs(LoginRequiredMixin,ListView):
    model = BlogItem
    template_name = "blogs/blogs.html"
    ordering = ['-blog_created_time']
    context_object_name = 'posts'
    login_url = 'signin'
    



class SpecificBlog(LoginRequiredMixin,DetailView):
    model = BlogItem
    template_name = "blogs/blog_info.html"
    context_object_name = "blog_info"
    slug_field = "blog_id"
    slug_url_kwarg = "blog_id"
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cm'] = BlogComment.objects.filter(blog_id=self.get_object())
        return context
       
    def post(self, request, *args, **kwargs):
        BlogComment(
                blog_id =  BlogItem.objects.get(blog_id=kwargs.get('blog_id')),
                blog_comment_user = request.user,
                blog_comment  = request.POST['comments'],
        ).save()
        return HttpResponseRedirect(self.request.path_info)
           
        

class CreateBlog(LoginRequiredMixin,CreateView):
    model = BlogItem
    template_name = "blogs/create_blog.html"
    fields =['blog_title', 'blog_description', 'blog_info']
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form)
        return super().form_valid(form)


@csrf_exempt
def deleteComment(request):
    try:
        commentDelete = json.loads(request.body)['data']
        #print(commentDelete)
        BlogComment.objects.filter(pk=commentDelete).delete()
    except Exception as err:
        print(err)
    return HttpResponse()
        

@csrf_exempt
def deleteBlog(request):
    try:
        blogDelete = json.loads(request.body)['data']
        #print(blogDelete)
        BlogItem.objects.filter(pk=blogDelete).delete()
    except Exception as err:
        print(err)
    return redirect('blogs')