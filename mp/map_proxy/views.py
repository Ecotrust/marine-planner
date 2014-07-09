from proxy.views import proxy_view


def mapproxy_view(request, path):
    headers = {
        "Host": "localhost:8000",
        "X-Script-Name": "/mapproxy"
    }

    remoteurl = 'http://127.0.0.1:8889/' + path
    return proxy_view(request, remoteurl, {"headers": headers})

