from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
import string,random
# Create your models here.
class BlogItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blogs')
    blog_title = models.CharField(max_length=180,unique=True)
    blog_description = models.CharField(max_length=500)
    blog_info = models.TextField()
    blog_created_time = models.DateTimeField(auto_now_add=True)
    blog_id= models.CharField(max_length=60,unique=True)
    #blog_image = models.ImageField(upload_to='blogmedia',null=True,blank=True)

    def generate_unique_id(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=6))

    def save(self, *args, **kwargs):
        if not self.blog_id:
            unique_id = self.generate_unique_id()
            while BlogItem.objects.filter(blog_id=unique_id).exists():
                unique_id = self.generate_unique_id()
            self.blog_id = unique_id
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.blog_title
    



class BlogComment(models.Model):
    blog_id = models.ForeignKey(BlogItem, on_delete=models.CASCADE)
    blog_comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_comment = models.TextField()
    blog_comment_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.blog_comment


    