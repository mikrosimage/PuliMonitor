import logging

from PyQt4.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt4.QtGui import QApplication, qApp
import requests

from octopus.core.enums.rendernode import RN_STATUS_NAMES
from pulimonitor.util.config import Config


requestHandler = None
requestThread = None


def getRequestHandler():
    global requestHandler
    global requestThread
    if not requestHandler:
        requestThread = QThread(qApp)
        requestHandler = RequestHandler()
        requestHandler.moveToThread(requestThread)
        requestThread.started.connect(requestHandler.start)
        requestThread.finished.connect(requestHandler.deleteLater)
        requestThread.start()
    return requestHandler


class RequestHandler(QObject):
    '''
    A class handling the requests to the puli server. Results from the server
    are published via specific signals. For each type of request/listener
    (e.g. the rendernodes query request and the rendernodes view) there is a
    separate signal. This QObject subclass is meant to run in its own Qthread,
    so the requests, json parsing and instance creation does not block the
    gui thread.
    '''

    renderNodesUpdated = pyqtSignal(list)
    renderNodesStatsChanged = pyqtSignal(list)
    poolsUpdated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(RequestHandler, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.config = Config(self)
        self.baseUrl = "http://{host}:{port}".format(host=self.config.hostname,
                                                     port=self.config.port)
        self.rnUrl = "{baseurl}/rendernodes".format(baseurl=self.baseUrl)
        self.poolUrl = "{baseurl}/pools".format(baseurl=self.baseUrl)
        self.jobUrl = "{baseurl}/tasks".format(baseurl=self.baseUrl)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.requestAll)

        self.renderNodesVisible = False
        self.poolsVisible = False

        self.__requestErrorLogged = False

    def start(self):
        self.log.debug("started")
        self.requestAll()
        self.timer.start(self.config.refreshInterval)

    def stop(self):
        self.log.debug("stopped")
        self.timer.stop()
        t = self.thread()
        t.quit()
        t.wait()

    def queryAllRenderNodes(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request render nodes")
        try:
            r = requests.get(self.rnUrl)
            self.__requestErrorLogged = False
        except:
            # log a request error only once
            if not self.__requestErrorLogged:
                self.log.exception("Query all rendernodes request to server failed.")
                return
        if r.status_code == 200:
            jsonData = r.json().get("rendernodes")
            self.renderNodesUpdated.emit(jsonData)
            stats = [("Total", len(jsonData))]

            statusCounts = {}
            for node in jsonData:
                sn = RN_STATUS_NAMES[node.get("status")]
                statusCounts[sn] = statusCounts.setdefault(sn, 0) + 1
            stats += sorted(statusCounts.items())
            self.renderNodesStatsChanged.emit(stats)
        else:
            self.log.error("Error querying for all rendernodes.")

    def queryAllPools(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request pools")
        try:
            r = requests.get(self.poolUrl)
            self.__requestErrorLogged = False
        except:
            # log a request error only once
            if not self.__requestErrorLogged:
                self.log.exception("Query all pools request to server failed.")
                return
        if r.status_code == 200:
            jsonData = r.json().get("pools", {}).values()
            self.poolsUpdated.emit(jsonData)
        else:
            self.log.error("Error querying for all pools.")

    def queryAllJobs(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request jobs")
        try:
            r = requests.get(self.jobUrl)
            self.__requestErrorLogged = False
        except:
            # log a request error only once
            if not self.__requestErrorLogged:
                self.log.exception("Query all jobs request to server failed.")
                return
        if r.status_code == 200:
            jsonData = r.json()
            print jsonData
        else:
            self.log.error("Error querying for all jobs.")

    def requestAll(self):
        '''
        Request all data
        '''
        self.log.debug("request all")
        self.queryAllRenderNodes()
        self.queryAllPools()

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
    rh = RequestHandler()
    rh.moveToThread(t)
    t.finished.connect(rh.deleteLater)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
