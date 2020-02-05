from django.shortcuts import render_to_response,render
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache
from .models import HomeImage

def get_sevendays_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gte=date).values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    if len(blogs)>0:
      return blogs[0]
    else:
      return None


def home(request):
    #获取七天的访问量
    blog_content_type = ContentType.objects.get_for_model(Blog)
    images=HomeImage.objects.all().order_by('stars')

    #选取最多五张的封面照片
    if len(images)>5:
        homeImages=images[:5]
    else:
        homeImages=images

    #获取热门七天的缓存数据
    hot_blogs_for_7days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7days is None:
      hot_blogs_for_7days = get_sevendays_hot_blogs()
      cache.set('hot_blogs_for_7_days',hot_blogs_for_7days,3600)

    context = {}
    context['sevendays_hot_data'] = hot_blogs_for_7days
    context['home_images']=homeImages
    return render(request, 'home/home.html', context)
