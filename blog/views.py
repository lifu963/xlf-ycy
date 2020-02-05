from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from .models import BlogType, Blog
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data


each_page_blog_number=4
# Create your views here.


def blog_common_data(request,blogs_all_list):
    #分页器
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    #页码原始范围
    page_range = list(range(max(current_page_num-2,1),current_page_num))+list(range(current_page_num,min(paginator.num_pages,current_page_num+2)+1))
    #加上省略页码标记
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')
    #加上首页/尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    # blogtype=BlogType.objects.all()
    #获取博客类型下的数量
    # blog_types_list=[]
    # for blog_type in blog_types:
    #     blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_type)
    # context['blog_types'] = blog_types_list
    blog_dates=Blog.objects.dates(field_name='create_time',kind='month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count
    context['blog_dates']=blog_dates_dict
    context['page_range']=page_range
    return context

def blog_charts(context):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    context['dates'] = dates
    context['read_nums'] = read_nums
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context=blog_common_data(request,blogs_all_list)
    context=blog_charts(context)
    return render(request,'blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context=blog_common_data(request,blogs_all_list)
    context = blog_charts(context)
    context['blog_type'] = blog_type
    return render(request,'blog/blog_with_type.html', context)

def blogs_with_date(request,year,month):
    context = {}
    blogs_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context=blog_common_data(request,blogs_all_list)
    context = blog_charts(context)
    context['blogs_with_date']='%s年%s月'%(year,month)
    return render(request,'blog/blog_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)

    context = {}
    context['previous_blog']=Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['blog']=blog
    context['next_blog']=Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render(request,'blog/blog_detail.html', context)
    age=24*60*60
    response.set_cookie(read_cookie_key,'true',max_age=age)
    return response