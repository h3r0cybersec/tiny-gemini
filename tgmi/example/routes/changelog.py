from tgmi.core.server import Route

class ChangeLogRoute(Route):
    """
        Rotta per la gestione di richieste su path: /
    """
    _routes = {
        "/changelog": "h_changelog",
    }
    
    def h_changelog(self):
        return self.response.success(meta=self.render_resource("changelog.gmi"))