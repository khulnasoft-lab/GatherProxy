* Supported version: [![](https://img.shields.io/badge/Python-2.7-green.svg)](https://docs.python.org/2.7/)
[![](https://img.shields.io/badge/Python-3.5-blue.svg)](https://docs.python.org/3.5/)
[![](https://img.shields.io/badge/Python-3.6-blue.svg)](https://docs.python.org/3.6/)
[![](https://img.shields.io/badge/Python-3.7-blue.svg)](https://docs.python.org/3.7/)
[![](https://img.shields.io/badge/Python-3.8-blue.svg)](https://docs.python.org/3.8/)
[![](https://img.shields.io/badge/Python-3.9-blue.svg)](https://docs.python.org/3.9/)
[![](https://img.shields.io/badge/Python-3.10-blue.svg)](https://docs.python.org/3.10/)
[![](https://img.shields.io/badge/Python-3.11-blue.svg)](https://docs.python.org/3.11/)

[![CodeFactor](https://www.codefactor.io/repository/github/khulnasoft-lab/gatherproxy/badge)](https://www.codefactor.io/repository/github/khulnasoft-lab/gatherproxy)

### Docker Image

```bash
docker pull khulnasoft/gatherproxy

docker run --env DB_CONN=redis://:password@ip:port/0 -p 5010:5010 khulnasoft/gatherproxy:latest
```
### docker-compose

Run in the project directory:
``` bash
docker-compose up -d
```
