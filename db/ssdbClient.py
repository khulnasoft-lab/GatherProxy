# -*- coding: utf-8 -*-
# !/usr/bin/env python
from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool
from handler.logHandler import LogHandler
from random import choice
from redis import Redis
import json


class SsdbClient(object):
    """
    SSDB client

    The structure of agent storage in SSDB is hash:
    The key is the proxy's ip:por, and the value is a dictionary of proxy attributes;
    """

    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
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
        Return a random proxy from the hash
        :return:
        """
        if https:
            items_dict = self.__conn.hgetall(self.name)
            proxies = list(
                filter(lambda x: json.loads(x).get("https"), items_dict.values())
            )
            return choice(proxies) if proxies else None
        else:
            proxies = self.__conn.hkeys(self.name)
            proxy = choice(proxies) if proxies else None
            return self.__conn.hget(self.name, proxy) if proxy else None

    def put(self, proxy_obj):
        """
        Put the proxy into the hash
        :param proxy_obj: Proxy obj
        :return:
        """
        result = self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)
        return result

    def pop(self, https):
        """
        Pop up an agent in sequence
        :return: proxy
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
        self.__conn.hdel(self.name, proxy_str)

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
        self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)

    def getAll(self, https):
        """
        Return all agents in dictionary form, use changeTable to specify hash name
        :return:
        """
        item_dict = self.__conn.hgetall(self.name)
        if https:
            return list(
                filter(lambda x: json.loads(x).get("https"), item_dict.values())
            )
        else:
            return item_dict.values()

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
        log = LogHandler("ssdb_client")
        try:
            self.getCount()
        except TimeoutError as e:
            log.error("ssdb connection time out: %s" % str(e), exc_info=True)
            return e
        except ConnectionError as e:
            log.error("ssdb connection error: %s" % str(e), exc_info=True)
            return e
        except ResponseError as e:
            log.error("ssdb connection error: %s" % str(e), exc_info=True)
            return e
