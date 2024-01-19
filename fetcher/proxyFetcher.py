# -*- coding: utf-8 -*-
import re
import json
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url, verify=False).tree
        latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[
            0
        ].strip()
        from datetime import datetime

        interval = datetime.now() - datetime.strptime(
            latest_page_time, "%Y/%m/%d %H:%M:%S"
        )
        if interval.seconds < 300:
            target_url = (
                "https://www.zdaye.com/"
                + html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
            )
            while target_url:
                _tree = WebRequest().get(target_url, verify=False).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = (
                    "https://www.zdaye.com/" + next_page[0].strip()
                    if next_page
                    else False
                )
                sleep(5)

    @staticmethod
    def freeProxy02():
        """
        http://www.66ip.cn/
        """
        url = "http://www.66ip.cn/"
        resp = WebRequest().get(url, timeout=10).tree
        for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
            if i > 0:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03():
        """Happy Agent"""
        target_urls = [
            "http://www.kxdaili.com/dailiip.html",
            "http://www.kxdaili.com/dailiip/2/1.html",
        ]
        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy04():
        """FreeProxyList https://www.freeproxylists.net/zh/"""
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
        tree = WebRequest().get(url, verify=False).tree
        from urllib import parse

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath("./td[1]/script/text()")).strip())
            port = "".join(tr.xpath("./td[2]/text()")).strip()
            if ip:
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=1):
        """https://www.kuaidaili.com"""
        url_pattern = [
            "https://www.kuaidaili.com/free/inha/{}/",
            "https://www.kuaidaili.com/free/intr/{}/",
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath(".//table//tr")
            sleep(1)
            for tr in proxy_list[1:]:
                yield ":".join(tr.xpath("./td/text()")[0:2])

    @staticmethod
    def freeProxy06():
        """FateZero http://proxylist.fatezero.org/"""
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.split("\n"):
                json_info = json.loads(each)
                if json_info.get("country") == "CN":
                    yield "%s:%s" % (
                        json_info.get("host", ""),
                        json_info.get("port", ""),
                    )
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07():
        urls = [
            "http://www.ip3366.net/free/?stype=1",
            "http://www.ip3366.net/free/?stype=2",
        ]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r"<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>",
                r.text,
            )
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        urls = ["https://ip.ihuan.me/address/5Lit5Zu9.html"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r">\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>",
                r.text,
            )
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        for i in range(1, page_count + 1):
            url = "http://ip.jiangxianli.com/?country=中国&page={}".format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10():
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r"<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>",
            r.text,
        )
        for proxy in proxies:
            yield ":".join(proxy)

    @staticmethod
    def freeProxy11():
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json["data"]:
                yield each["ip"]
        except Exception as e:
            print(e)


if __name__ == "__main__":
    p = ProxyFetcher()
    for _ in p.freeProxy11():
        print(_)

# http://nntime.com/proxy-list-01.htm


# freeProxy04
# freeProxy07
# freeProxy08
