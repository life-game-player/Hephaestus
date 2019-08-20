from rpyc.utils.server import ThreadedServer

from services.kos import Kos


t = ThreadedServer(Kos, port=18861)
t.start()
