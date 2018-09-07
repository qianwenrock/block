from django.core.cache import cache
from common import rds
from post.models import Post
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

def read_count(func):
    def wrapper(request):
        post_id = int(request.GET.get('post_id'))
        # 对每篇的帖子进行加计数
        rds.zincrby('readrank',post_id)
        return func(request)
    return wrapper

def top_n(num):
    # 从redis中获取原始的数据
    ori_data = rds.zrevrange(b'readrank', 0, num-1, withscores=True)
    # 清洗数据  将数据装换成整形
    cleaned_rank = [[int(post_id),int(count)] for post_id, count in ori_data]
    # 思路一：直接替换
    # for item in cleaned_rank:
    #     item[0] = Post.objects.get(id=item[0])
    # rank_data = cleaned_rank

    # 思路二：批量获取 Post
    # post_id_list = [post_id for post_id, _ in cleaned_rank]
    # posts = Post.objects.filter(id__in=post_id_list)  # 批量取出 posts
    # posts = sorted(posts, key=lambda post: post_id_list.index(post.id))  # 调整为正确的顺序
    # # 组装 rank_data
    # rank_data = []
    # 遍历获取帖子和点击量
    # for post, (_, count) in zip(posts, cleaned_rank):
    #     rank_data.append([post, count])

    # 思路三
    post_id_list = [post_id for post_id, _ in cleaned_rank]
    # post_dict = {
    #     1: <Post: Post object>,
    #     3: <Post: Post object>,
    #     29: <Post: Post object>,
    # }
    post_dict = Post.objects.in_bulk(post_id_list)  # 批量获取 post 字典
    for item in cleaned_rank:
        post_id = item[0]
        item[0] = post_dict[post_id]
    rank_data = cleaned_rank

    return rank_data