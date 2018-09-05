from django.core.cache import cache

def page_cach(timeout):
    def wrapper(func):
        def inner(request):
            # 通过session_key 和get_full_path()将用户和函数进行分开
            key = 'PageCache-%s-%s'%(request.session.session_key,request.get_full_path())
            response = cache.get(key)
            # 判断缓存中是否有这个数据
            if response is None:
                # 没有 则去数据库中取
                response = func(request)
                # 将数据添加到缓存中
                cache.set(key,response,timeout)
            return response
        return inner
    return wrapper
