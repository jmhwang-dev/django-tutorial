from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

# Create your views here.
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self,):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip() # 선행과 후행 문자가 제거된 문자열의 복사본을 return
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()   # 앞,뒤 공백 제거
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if  is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            
            return response
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
def category_page(request, slug):
    if slug == "no_category":
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category
        }
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count()
        }
    )