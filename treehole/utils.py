from .models import Saying
import random

def get_defender_key(request):
    key = "%s_agreed" % request.user
    return key

def randSaying():
    sayings=Saying.objects.all()
    sayings_count=len(sayings)
    if sayings_count==0:
        return None
    randNum = random.randint(0,sayings_count-1)
    return sayings[randNum]

#一个函数：统计某字符串除去忽略字符的长度
def CountChar(m_str,igs):
    count=0
    for ig in igs:
        count+=m_str.count(ig)
    return len(m_str)-count

def clearSayings(sayings):
    sayings_end=[]
    for saying_o in sayings.split('.'):
        if CountChar(saying_o,igs=(' ',','))<=12:
            sayings_end.append(saying_o)
        else:
            # '我是猪,我是猪,我是猪,我是猪,我是猪'
            for saying_t in saying_o.split(','):
                if CountChar(saying_t,' ')<=12:
                    sayings_end.append(saying_t)
                else:
                    for saying_th in saying_t.split(' '):
                        if len(saying_th)<=12:
                            sayings_end.append(saying_th)
    for saying_end in sayings_end:
        if saying_end=='':
            sayings_end.remove(saying_end)
    return sayings_end