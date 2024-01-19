# -*- coding: utf-8 -*-
import json


class Proxy(object):
    def __init__(
        self,
        proxy,
        fail_count=0,
        region="",
        anonymous="",
        source="",
        check_count=0,
        last_status="",
        last_time="",
        https=False,
    ):
        self._proxy = proxy
        self._fail_count = fail_count
        self._region = region
        self._anonymous = anonymous
        self._source = source.split("/")
        self._check_count = check_count
        self._last_status = last_status
        self._last_time = last_time
        self._https = https

    @classmethod
    def createFromJson(cls, proxy_json):
        _dict = json.loads(proxy_json)
        return cls(
            proxy=_dict.get("proxy", ""),
            fail_count=_dict.get("fail_count", 0),
            region=_dict.get("region", ""),
            anonymous=_dict.get("anonymous", ""),
            source=_dict.get("source", ""),
            check_count=_dict.get("check_count", 0),
            last_status=_dict.get("last_status", ""),
            last_time=_dict.get("last_time", ""),
            https=_dict.get("https", False),
        )

    @property
    def proxy(self):
        """acting ip:port"""
        return self._proxy

    @property
    def fail_count(self):
        """Detection failures"""
        return self._fail_count

    @property
    def region(self):
        """Geographical location (country/city)"""
        return self._region

    @property
    def anonymous(self):
        """Anonymous"""
        return self._anonymous

    @property
    def source(self):
        """proxy source"""
        return "/".join(self._source)

    @property
    def check_count(self):
        """Number of proxy detections"""
        return self._check_count

    @property
    def last_status(self):
        """Last detection result True -> available; False -> not available"""
        return self._last_status

    @property
    def last_time(self):
        """Last detection time"""
        return self._last_time

    @property
    def https(self):
        """Does it support https"""
        return self._https

    @property
    def to_dict(self):
        """attribute dictionary"""
        return {
            "proxy": self.proxy,
            "https": self.https,
            "fail_count": self.fail_count,
            "region": self.region,
            "anonymous": self.anonymous,
            "source": self.source,
            "check_count": self.check_count,
            "last_status": self.last_status,
            "last_time": self.last_time,
        }

    @property
    def to_json(self):
        """Attribute json format"""
        return json.dumps(self.to_dict, ensure_ascii=False)

    @fail_count.setter
    def fail_count(self, value):
        self._fail_count = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value

    @https.setter
    def https(self, value):
        self._https = value

    @region.setter
    def region(self, value):
        self._region = value

    def add_source(self, source_str):
        if source_str:
            self._source.append(source_str)
            self._source = list(set(self._source))
