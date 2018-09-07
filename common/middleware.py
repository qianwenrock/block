from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
import time




class BlockMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # 获取用户IP
        user_id = request.META['REMOTE_ADDR']
        request_key = 'RequestTime-%s'%user_id
        block_key = 'Blocker-%s'%user_id
        # 判断封禁中有没有正在使用的IP
        if cache.get(block_key):
            return render(request,'blockers.html')
        # 获取最新的访问时间戳
        now = time.time()
        # 没有就给默认时间
        t0, t1, t2 = cache.get(request_key,[0,0,0])
        # 对访问频率进行判断
        if (now - t0) < 1:
            # 设置封禁时间24小时
            cache.set(block_key,1,86400)
            return render(request,'blockers.html')
        else:
            # 更新缓存中存储的访问时间
            cache.set(request_key,[t1,t2,now])


