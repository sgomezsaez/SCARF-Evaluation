class WorkloadOcurrence:
    def __init__(self, timeStamp, numberRequests, sizeContentBytes):
        self.timeStamp = timeStamp
        self.numberRequests = numberRequests
        self.sizeContentBytes = sizeContentBytes

    def getNumberRequests(self):
        return self.numberRequests

    def getSizeContentBytes(self):
        return self.sizeContentBytes

    def addNumberRequests(self, requests):
        self.numberRequests += requests

    def addSizeContentBytes(self, size):
        self.sizeContentBytes += size

    def __str__(self):
        return str(self.timeStamp) + ' ' + str(self.numberRequests) + ' ' + str(self.sizeContentBytes)