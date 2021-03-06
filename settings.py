from PyQt4 import QtCore
from logging import getLogger

LOGGER = getLogger(__name__)

QtCore.QCoreApplication.setOrganizationName('Adam')
QtCore.QCoreApplication.setOrganizationDomain('dagobah.com')
QtCore.QCoreApplication.setApplicationName('TaskList')

class Settings:
    def __init__(self, prefix):
        self.prefix = prefix
    def __enter__(self):
        self.settings = QtCore.QSettings()
        LOGGER.info("Looking in %s" % self.prefix)
        self.settings.beginGroup(self.prefix)
        return self.settings
    def __exit__(self, *args, **kwargs):
        LOGGER.info("endGroup")
        self.settings.endGroup()

class AppSettings(object):
    prefix = None
    
    def __init__(self):
        if not self.prefix:
            self.prefix = str(self.__class__.__name__)
    
    def __getattribute__(self, name):
        if name.isupper():
            LOGGER.info("get %s/%s" % (self.prefix, name))
            with Settings(self.prefix) as settings:
                if settings.contains(name):
                    return settings.value(name)
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, value):
        if name.isupper():
            LOGGER.info("set %s/%s" % (self.prefix, name))
            with Settings(self.prefix) as settings:
                settings.setValue(name, value)
        object.__setattr__(self, name, value)
    
