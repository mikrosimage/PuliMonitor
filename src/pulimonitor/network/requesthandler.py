"""
The RequestHandler is a singleton class, that lives in a separate QThread. It
is responsible for pulling data from the server in intervals (specified in the
configuration) as well as on demand. It is also used to communicate user actions
to the server.
"""

import json
import logging

from PyQt4.QtCore import QObject, pyqtSignal, QTimer, QThread, QSettings
from PyQt4.QtGui import QApplication, qApp
import requests

from octopus.core.enums.rendernode import RN_STATUS_NAMES
from puliclient.server.queueHandler import QueueHandler
from puliclient.server.renderNodeHandler import RenderNodeHandler
from puliclient.server.server import Server
from pulimonitor.util import config


def get(refresh=False):
    '''
    Create the RequestHandler and move it to its own QThread.
    '''
    if refresh:
        get.requestHandler = None
    if get.requestHandler:
        return get.requestHandler

    get.requestThread = QThread(qApp)
    get.requestHandler = RequestHandler()
    get.requestHandler.moveToThread(get.requestThread)
    get.requestThread.started.connect(get.requestHandler.start)
    get.requestThread.finished.connect(get.requestHandler.deleteLater)
    return get.requestHandler

get.requestHandler = None
get.requestThread = None


def startRequestThread():
    '''
    Starts the request thread.
    '''
    get.requestThread.start()


class RequestHandler(QObject):
    '''
    A class handling the requests to the puli server. Results from the server
    are published via specific signals. For each type of request/listener
    (e.g. the rendernodes query request and the rendernodes view) there is a
    separate signal. This QObject subclass is meant to run in its own QThread,
    so the requests, json parsing and instance creation does not block the
    GUI thread.
    '''

    renderNodesUpdated = pyqtSignal(list)
    renderNodesStatsChanged = pyqtSignal(list)
    poolsUpdated = pyqtSignal(list)
    jobsUpdated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(RequestHandler, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.requestHandler = config.get()
        self.servers = []
        self.currentServer = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.requestAll)
        self.__requestErrorLogged = False
        self.renderNodeHandler = None
        self.poolHandler = None
        self.queueHandler = None

    def loadSettings(self):
        '''
        Loads the settings for the RequestHandler. This includes:
           * The server used last
        '''
        settings = QSettings()
        settings.beginGroup("requestHandler")
        lastServer = int(settings.value("last_server", 0))
        try:
            self.currentServer = self.servers[lastServer]
            self.log.info("Current server is %s" % self.currentServer)
        except IndexError:
            pass
        settings.endGroup()

    def onServerChanged(self, server):
        '''
        Slot called if the server is changed. Propagates this change to the
        different handlers.
        '''
        self.renderNodeHandler.setServer(server)
#         self.poolHandler.setServer(server)
#         self.queueHandler.setServer(server)
        self.log.info("Server set to: %s" % server)

    def loadServers(self):
        '''
        Loads Server definitions from the configuration.
        '''
        for hostname, port in self.requestHandler.items("Servers"):
            server = Server(hostname, port)
            server.online = False
            self.servers.append(server)

    def challengeServers(self):
        '''
        This function tries to connect to the server configured in settings.ini

        :returns: list -- list of names of all offline servers
        '''
        for server in self.servers:
            try:
                # TODO:replace this with a different call to the server
                server.get("pools")
                server.online = True
                self.log.info("%s is online" % server)
            except:
                self.log.info("%s is offline" % server)

    def offlineServers(self):
        '''
        :returns: `Server` -- all offline :class:`Server` instances.
        '''

        return [s for s in self.servers if not s.online]

    def start(self):
        self.log.debug("started")
        self.requestAll()
        self.timer.start(self.requestHandler.getint("General", "refresh_interval") * 1000)

    def stop(self):
        self.log.debug("stopped")
        self.timer.stop()
        t = self.thread()
        t.quit()
        t.wait()

    def setRenderNodesPaused(self, rendernodes, paused, kill):
        if self.currentServer:
            erroneous = []
            for rn in rendernodes:
                r = self.currentServer.put("rendernodes/{name}/paused/".format(name=rn.name),
                                           data=json.dumps({"paused": paused, "killproc": kill}))
                if r == "":
                    self.log.info("(un)paused " + rn.name)
                else:
                    self.log.error("error (un)pausing " + rn.name)
                    erroneous.append(rn.name)
            return erroneous
        else:
            return False

    def queryAllRenderNodes(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request render nodes")

        if not self.renderNodeHandler:
            if self.currentServer:
                self.renderNodeHandler = RenderNodeHandler(self.currentServer)
            else:
                return

        rendernodes = ()
        try:
            rendernodes = self.renderNodeHandler.getAllRenderNodes()[0]
        except:
            self.timer.stop()

        self.renderNodesUpdated.emit(rendernodes)
        stats = [("Total", len(rendernodes))]
        statusCounts = {}
        for rendernode in rendernodes:
            statusName = RN_STATUS_NAMES[rendernode.status]
            statusCounts[statusName] = statusCounts.setdefault(statusName, 0) + 1
        stats += sorted(statusCounts.items())
        self.renderNodesStatsChanged.emit(stats)

    def queryAllPools(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request pools")

        if not self.poolHandler:
            self.poolHandler = None

        pools = []
        try:
            pools = []
        except:
            self.timer.stop()

        self.poolsUpdated.emit(pools)

    def queryAllJobs(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request jobs")
        if not self.queueHandler:
            self.queueHandler = QueueHandler()

        jobs = []
        try:
            jobs = self.queueHandler.getAllJobs(False)
        except:
            self.timer.stop()
        self.jobsUpdated.emit(jobs)

    def requestAll(self):
        '''
        Request all data
        '''
        self.log.debug("request all")
        self.queryAllRenderNodes()
        # self.queryAllPools()

    def addPool(self, name):
        self.log.debug("add pool " + name)
        try:
            r = requests.post(self.poolUrl + "/" + name)
            self.__requestErrorLogged = False
        except:
            # log a request error only once
            if not self.__requestErrorLogged:
                self.log.exception("Add pool request to server failed.")
                return
        if r.status_code == 200:
            return True
        else:
            self.log.error("Error posting new pool:" + name)

    def deletePool(self, name):
        self.log.debug("delete pool " + name)
        try:
            r = requests.delete(self.poolUrl + "/" + name)
            self.__requestErrorLogged = False
        except:
            # log a request error only once
            if not self.__requestErrorLogged:
                self.log.exception("Deleting pool request to server failed.")
                return
        if r.status_code == 200:
            return True
        else:
            self.log.error("Error deleting pool:" + name)


def main():
    import sys
    app = QApplication([])
    t = QThread()
    rh = _RequestHandler()
    rh.moveToThread(t)
    t.finished.connect(rh.deleteLater)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
