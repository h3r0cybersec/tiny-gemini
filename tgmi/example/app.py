from tgmi.core.server import GeminiServer
from routes import index, changelog
import logging

log = logging.getLogger("rich")
log.setLevel(logging.NOTSET)


if __name__ == "__main__":
    try:
        with GeminiServer() as server:
            # add routes
            server.add_route(index.IndexRoute())
            server.add_route(changelog.ChangeLogRoute())
            # run server
            server.serve_forever()
    except KeyboardInterrupt:
        log.warning("[-] server is down")
    