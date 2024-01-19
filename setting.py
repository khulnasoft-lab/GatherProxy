# -*- coding: utf-8 -*-
VERSION = "2.4.0"

# ############### server config ###############
HOST = "0.0.0.0"

PORT = 5010

# ############### database config ###################
# db connection uri
# example:
#      Redis: redis://:password@ip:port/db
#      Ssdb:  ssdb://:password@ip:port
DB_CONN = "redis://:pwd@127.0.0.1:6379/0"

# proxy table name
TABLE_NAME = "use_proxy"


# ###### config the proxy fetch function ######
PROXY_FETCHER = [
    "freeProxy01",
    "freeProxy02",
    "freeProxy03",
    "freeProxy04",
    "freeProxy05",
    "freeProxy06",
    "freeProxy07",
    "freeProxy08",
    "freeProxy09",
    "freeProxy10",
    "freeProxy11",
]

# ############# proxy validator #################
# Proxy authentication target website
HTTP_URL = "http://httpbin.org"

HTTPS_URL = "https://www.qq.com"

# Timeout during proxy verification
VERIFY_TIMEOUT = 10

# The maximum number of failures allowed in nearly PROXY_CHECK_COUNT verifications. If it exceeds the maximum number of failures, the proxy will be removed.
MAX_FAIL_COUNT = 0

# The maximum failure rate allowed in the recent PROXY_CHECK_COUNT verification, if it exceeds, the proxy will be removed
# MAX_FAIL_RATE = 0.1

# When proxyCheck, the number of proxies is less than POOL_SIZE_MIN to trigger crawling
POOL_SIZE_MIN = 20

# ############# proxy attributes #################
# Whether to enable the proxy region attribute
PROXY_REGION = True

# ############# scheduler config #################

# Set the timezone for the scheduler forcely (optional)
# If it is running on a VM, and
#   "ValueError: Timezone offset does not match system offset"
#   was raised during scheduling.
# Please uncomment the following line and set a timezone for the scheduler.
# Otherwise it will detect the timezone from the system automatically.

TIMEZONE = "Asia/Dhaka"
