import time

class Time():

    _elapseTime_db = []
    _startTime = None

    def start(self):
        self._startTime = time.time()

    def elapse(self):
        if self._startTime is None:
            return None
        
        self._elapseTime_db.append(time.time())
        return (self._elapseTime_db[len(self._elapseTime_db)-1] - self._startTime)

    def clear(self):
        self._elapseTime_db = []
        self._startTime = None