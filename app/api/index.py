routes = [
    {
        "path": "/helloworld",
        "name": "哈囉世界",
    },
    {
        "path": "/helloworld2",
        "name": "哈囉世界2",
    },
    {
        "path": "/api/test",
        "name": "測試",
    },
]


class createRouter:
    def __init__(self, routes: list):
        self.routes = routes

    def get(self, path):
        for route in routes:
            if route["path"] == path:
                return route["name"]
        raise ValueError("No route found")


router = createRouter(routes=routes)
