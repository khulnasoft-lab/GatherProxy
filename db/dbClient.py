# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys

from util.six import urlparse, withMetaclass
from util.singleton import Singleton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DbClient(withMetaclass(Singleton)):
    """
    DbClient DB factory class provides get/put/update/pop/delete/exists/getAll/clean/getCount/changeTable methods


    Abstract method definition：
        get(): randomly returns a proxy;
        put(proxy): store a proxy;
        pop(): returns and deletes a proxy in sequence;
        update(proxy): Update the specified proxy information;
        delete(proxy): delete the specified proxy;
        exists(proxy): Determine whether the specified proxy exists;
        getAll(): returns all agents;
        clean(): clear all proxy information;
        getCount(): returns proxy statistics;
        changeTable(name): switch operation object


        All methods need to be implemented by corresponding classes:
            ssdb: ssdbClient.py
            redis: redisClient.py
            mongodb: mongodbClient.py

    """

    def __init__(self, db_conn):
        """
        init
        :return:
        """
        self.parseDbConn(db_conn)
        self.__initDbClient()

    @classmethod
    def parseDbConn(cls, db_conn):
        db_conf = urlparse(db_conn)
        cls.db_type = db_conf.scheme.upper().strip()
        cls.db_host = db_conf.hostname
        cls.db_port = db_conf.port
        cls.db_user = db_conf.username
        cls.db_pwd = db_conf.password
        cls.db_name = db_conf.path[1:]
        return cls

    def __initDbClient(self):
        """
        init DB Client
        :return:
        """
        __type = None
        if "SSDB" == self.db_type:
            __type = "ssdbClient"
        elif "REDIS" == self.db_type:
            __type = "redisClient"
        else:
            pass
        assert __type, "type error, Not support DB type: {}".format(self.db_type)
        self.client = getattr(__import__(__type), "%sClient" % self.db_type.title())(
            host=self.db_host,
            port=self.db_port,
            username=self.db_user,
            password=self.db_pwd,
            db=self.db_name,
        )

    def get(self, https, **kwargs):
        return self.client.get(https, **kwargs)

    def put(self, key, **kwargs):
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value, **kwargs)

    def delete(self, key, **kwargs):
        return self.client.delete(key, **kwargs)

    def exists(self, key, **kwargs):
        return self.client.exists(key, **kwargs)

    def pop(self, https, **kwargs):
        return self.client.pop(https, **kwargs)

    def getAll(self, https):
        return self.client.getAll(https)

    def clear(self):
        return self.client.clear()

    def changeTable(self, name):
        self.client.changeTable(name)

    def getCount(self):
        return self.client.getCount()

    def test(self):
        return self.client.test()
