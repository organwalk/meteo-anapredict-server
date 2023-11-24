"""
    定义配置信息
    by organwalk 2023-08-15
"""
import pymysql
from collections import OrderedDict
from nacos import NacosClient
import threading
import time

_MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'meteo_data'
}


REDIS_CONFIG = {
    'host': 'localhost',
    'port': '6379',
    'db': '2',
    'password': '123456'
}


def get_mysql_obj():
    """
    返回MySQL的游标对象

    :return:
        object: MySQL游标对象

    by organwalk 2023-08-15
    """
    cnx = pymysql.connect(**_MYSQL_CONFIG)
    return cnx.cursor()


_NACOS_CONFIG = OrderedDict([
    ('service_name', 'meteo-anapredict-resource'),
    ('ip', 'localhost'),
    ('port', 9594),
    ('weight', 1.0)
])


def register_to_nacos() -> None:
    """
    注册服务至nacos

    :return:
        None: 开启一个新的线程向nacos发送心跳包

    by organwalk 2023-08-15
    """
    client = NacosClient('localhost:8848')
    client.add_naming_instance(**_NACOS_CONFIG)
    heartbeat_thread = threading.Thread(target=__send_heartbeat_periodically, args=(client,), daemon=True)
    heartbeat_thread.start()


def __send_heartbeat_periodically(client: NacosClient):
    """
    每十秒发送一次心跳至nacos

    :param client: nacos服务中心
    :return:
        None: 每十秒发送一次心跳至nacos

    by organwalk 2023-08-15
    """
    first_run = True
    while True:
        first_run = False if first_run else time.sleep(10)
        client.send_heartbeat(**_NACOS_CONFIG)
