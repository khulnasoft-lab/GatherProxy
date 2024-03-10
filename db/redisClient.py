# -*- coding: utf-8 -*-

from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool
from handler.logHandler import LogHandler
from random import choice
from redis import Redis
import json


class RedisClient(object):
    """
    Redis client

    The proxy storage structure in Redis is hash:
    The key is ip:port, and the value is a dictionary of proxy attributes;

    """

    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.name = ""
        kwargs.pop("username")
        self.__conn = Redis(
            connection_pool=BlockingConnectionPool(
                decode_responses=True, timeout=5, socket_timeout=5, **kwargs
            )
        )

    def get(self, https):
        """
        return a proxy
        :return:
        """
        if https:
            items = self.__conn.hvals(self.name)
            proxies = list(filter(lambda x: json.loads(x).get("https"), items))
            return choice(proxies) if proxies else None
        else:
            proxies = self.__conn.hkeys(self.name)
            proxy = choice(proxies) if proxies else None
            return self.__conn.hget(self.name, proxy) if proxy else None

    def put(self, proxy_obj):
        """
        Put the agent into the hash and use changeTable to specify the hash name
        :param proxy_obj: Proxy obj
        :return:
        """
        data = self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)
        return data

    def pop(self, https):
        """
        pop up a proxy
        :return: dict {proxy: value}
        """
        proxy = self.get(https)
        if proxy:
            self.__conn.hdel(self.name, json.loads(proxy).get("proxy", ""))
        return proxy if proxy else None

    def delete(self, proxy_str):
        """
        Remove the specified agent, use changeTable to specify the hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hdel(self.name, proxy_str)

    def exists(self, proxy_str):
        """
        Determine whether the specified agent exists, use changeTable to specify the hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, proxy_str)

    def update(self, proxy_obj):
        """
        Update the proxy attribute
        :param proxy_obj:
        :return:
        """
        return self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)

    def getAll(self, https):
        """
        Return all agents in dictionary form, use changeTable to specify hash name
        :return:
        """
        items = self.__conn.hvals(self.name)
        if https:
            return list(filter(lambda x: json.loads(x).get("https"), items))
        else:
            return items

    def clear(self):
        """
        Clear all proxies and use changeTable to specify hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def getCount(self):
        """
        Return the number of agents
        :return:
        """
        proxies = self.getAll(https=False)
        return {
            "total": len(proxies),
            "https": len(list(filter(lambda x: json.loads(x).get("https"), proxies))),
        }

    def changeTable(self, name):
        """
        switch operand
        :param name:
        :return:
        """
        self.name = name

    def test(self):
        log = LogHandler("redis_client")
        try:
            self.getCount()
        except TimeoutError as e:
            log.error("redis connection time out: %s" % str(e), exc_info=True)
            return e
        except ConnectionError as e:
            log.error("redis connection error: %s" % str(e), exc_info=True)
            return e
        except ResponseError as e:
            log.error("redis connection error: %s" % str(e), exc_info=True)
            return e
