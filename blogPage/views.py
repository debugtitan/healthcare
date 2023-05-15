
from django.shortcuts import redirect, render,HttpResponseRedirect,HttpResponse
from django.views.generic import ListView,TemplateView
from .models import BlogItem,BlogComment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from frontend.views import logging
from django.db.models import Count
import json



# Create your views here.

@method_decorator(login_required(login_url='signin'), name='dispatch')
class Blogs(ListView):
    model = BlogItem
    template_name = "blogs/blogs.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-blog_created_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = self.get_queryset()[:5]
        context['comments_total'] = BlogItem.objects.annotate(comment_count=Count('blogcomment')).values('comment_count')
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class SpecificBlog(ListView):
    model = BlogComment
    template_name = "blogs/blog_info.html"

    def get(self, request,**kwargs):
        try:
            blog_item = BlogItem.objects.get(blog_id=kwargs.get('blog_id'))
            cm =  BlogComment.objects.filter(blog_id=blog_item).order_by('-blog_comment_time')
            data = {
                 "comments": cm, #query all comments for the specific blog this user clicked
                 "blog_info": blog_item,
                 "count": BlogComment.objects.filter(blog_id=blog_item).count()
            }

            return render(request, self.template_name, data)
        except BlogItem.DoesNotExist:
                return redirect('blogs')
        
    def post(self,request,*args, **kwargs):
        try:
            logging.info(f"Comment: {request.POST['comments']} for blog: {kwargs.get('blog_id')}")
            comment = BlogComment(
                blog_id =  BlogItem.objects.get(blog_id=kwargs.get('blog_id')),
                blog_comment_user = request.user,
                blog_comment  = request.POST['comments'],
            )
            comment.save()
            blog_item = BlogItem.objects.get(blog_id=kwargs.get('blog_id'))
            cms =BlogComment.objects.filter(blog_id=blog_item).order_by('-blog_comment_time')
            data = {
                    "comments": cms, #query all comments for the specific blog this user clicked
                    "blog_info": blog_item,
                    "count": BlogComment.objects.filter(blog_id=blog_item).count()
            }
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
        except Exception as err:
            logging.warn(f'error save comment {err}')
            redirect('blogs')
        

class CreateBlog(TemplateView):
    template_name = "blogs/create_blog.html"
    

    def post(self,request):
        try:
            inData= json.loads(request.body)
            print(inData)
            blog_item = BlogItem(
                user=request.user, 
                blog_title=inData['title'], 
                blog_description=inData['desc'], 
                blog_info=inData['contents']
            )
            blog_item.save()
            
        except Exception as error:
            logging.warning(f"Create Blog error: {error}")
        return HttpResponse()