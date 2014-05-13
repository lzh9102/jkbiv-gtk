from baseapp import BaseApplication

class Application(BaseApplication):

    def onKeyPress(self, keystr):
        print "key: %s" % keystr
