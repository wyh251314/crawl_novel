# 代理池
# 源码地址：https://github.com/jiangxianli/ProxyIpLib#%E5%85%8D%E8%B4%B9%E4%BB%A3%E7%90%86ip%E5%BA%93
# 可用

import json
import requests

from typing import List

class PROXIES:
    """
        获取代理ip地址的类
    """
    def __init__(self) -> None:
        # 获取一个代理IP接口
        self.ip_url = "https://ip.jiangxianli.com/api/proxy_ip"
        # 获取多个代理IP接口
        self.ips_url = "https://ip.jiangxianli.com/api/proxy_ips"

    def get_useful_ip(self):
        """获取一个可用的代理ip"""

        res = requests.get(self.ip_url).text
        resp_json = json.loads(res)
        # print(resp_json)

        ip = resp_json.get("data",None).get("ip", None)
        port = resp_json.get("data",None).get("port", None)
        result = str(ip)+ ":" + str(port)
        return result

    def get_pool(self) -> List:
        """获取多个可用的代理ip"""

        re = requests.get(self.ips_url).text
        resp_json = json.loads(re)
        # print(resp_json)

        proxy_list = []
        data = resp_json.get("data", None).get("data", None)
        for i in data:
            ip = i.get("ip", None)
            port = i.get("port", None)
            proxy_list.append(str(ip) + ":" + str(port))
        return proxy_list


pool_lists = PROXIES()
print(pool_lists.get_pool())