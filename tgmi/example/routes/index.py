from tgmi.core.server import Route

class IndexRoute(Route):
    """
        Rotta per la gestione di richieste su path: /
    """
    _routes = {
        "/": "h_index",
        "/index": "h_index"
    } 

    def h_index(self):
        return self.response.success(
            meta=self.render_resource("index.gmi", params={
                "server": self.server.meta.version()
            })
        )