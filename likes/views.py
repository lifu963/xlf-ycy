from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from .models import LikeCount,LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

def ErrorResponse(code,message):
    data={}
    data['status']='ERROR'
    data['code']=code
    data['message']=message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data={}
    data['status'] = 'SUCCESS'
    data['liked_num']=liked_num
    return JsonResponse(data)

# Create your views here.
def like_change(request):
    #获取数据
    user=request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'you were not login')

    content_type=request.GET.get('content_type')
    object_id=int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'Object not exist')

    #处理数据
    if request.GET.get('is_like') == 'true':
        #未active,要点赞
        like_record,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created:
            #该用户没点赞过
            like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.likednum+=1
            like_count.save()
            return SuccessResponse(like_count.likednum)
        else:
            return ErrorResponse(402,"you were liked")
    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():#若点赞记录存在
            #有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.likednum -= 1
                like_count.save()
                return SuccessResponse(like_count.likednum)
            else:
                return ErrorResponse(404,'data error')
        else:
            #没点赞过
            return ErrorResponse(403,'you were not liked')

