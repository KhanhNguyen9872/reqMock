from .reqMock import *


for reqMock in ["__name__", "__file__", "__cached__", "__spec__", "__loader__", "__doc__", "__path__"]:
    globals()[reqMock] = __import__('requests').__dict__[reqMock]

del reqMock