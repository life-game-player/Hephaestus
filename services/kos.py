import rpyc


class Kos(rpyc.Service):
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_get_environments(self):
        return ['开发环境', '测试环境', '生产环境']
