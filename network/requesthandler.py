import logging

from PyQt4.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt4.QtGui import QApplication
import requests

from util.config import Config


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

    def __init__(self, parent=None):
        super(RequestHandler, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.config = Config(self)
        self.rnUrl = "http://{host}:{port}/rendernodes".format(host=self.config.hostname,
                                                               port=self.config.port)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.requestAll)

    def start(self):
        self.log.debug("started")
        self.requestAll()
        self.timer.start(self.config.refreshInterval)

    def stop(self):
        self.log.debug("stopped")
        self.timer.stop()

    def queryAllRenderNodes(self):
        '''
        Retrieves all render nodes from the server and publishes the data via the
        renderNodesUpdated signal.
        '''
        self.log.debug("request render nodes")
        r = requests.get(self.rnUrl)
        if r.status_code == 200:
            jsonData = r.json().get("rendernodes")
            self.renderNodesUpdated.emit(jsonData)
        else:
            self.log.error("Error querying for all rendernodes.")

    def requestAll(self):
        '''
        Request all data
        '''
        self.log.debug("request all")
        self.queryAllRenderNodes()


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
