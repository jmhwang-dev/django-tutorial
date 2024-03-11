from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post
    template_name = "blog/index.html"   # 기본 템플릿 지정 방법1
    
def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post
        }
    )