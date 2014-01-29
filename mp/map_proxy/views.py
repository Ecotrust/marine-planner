import proxy.views


def proxy_view(request, path):
    headers = {
        "Host": "localhost:8000",
        "X-Script-Name": "/mapproxy"
    }

    remoteurl = 'http://127.0.0.1:8889/' + path
    return proxy.views.proxy_view(request, remoteurl, {"headers": headers})
