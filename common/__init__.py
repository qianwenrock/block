from django.conf import settings

from redis import Redis

# 通过**将REDIS里的数据当参数
rds = Redis(**settings.REDIS)  # 创建全局的 redis 连接实例
