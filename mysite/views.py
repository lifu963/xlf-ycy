from blog.models import Blog
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

def search(request):
    search_words = request.GET.get('word','').strip()
    condition=None
    search_blogs=[]
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    if condition is not None:
      search_blogs = Blog.objects.filter(condition)
    paginator = Paginator(search_blogs,10)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)
    context={}
    context['search_words'] = search_words
    context['page_of_blogs'] = page_of_blogs
    context['search_blogs_count']=search_blogs.count()
    return render(request,'search.html',context)