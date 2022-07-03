#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

import threading
import time


class RateLimiter:
    def __init__(self, rate, max_burst, initial_burst=None, timefunc=None):
        self.rate = rate
        self.max_burst = max_burst
        self.bucket = max_burst if initial_burst is None else initial_burst
        self.timefunc = timefunc or time.time
        self.last_call = self.timefunc()
        self.lock = threading.Lock()

    def _fill_bucket(self):
        now = self.timefunc()
        if self.bucket < self.max_burst:
            self.bucket += self.rate * (now - self.last_call)
            if self.bucket > self.max_burst:
                self.bucket = self.max_burst
        self.last_call = now

    def try_acquire(self):
        """Non-blocking acquire for time slot.

        Returns a 2-tuple of:

            - Boolean flag of success.

            - Time (number of seconds) to sleep before next try, if acquire was
              unsuccessful.
        """
        with self.lock:
            self._fill_bucket()
            if self.bucket >= 1:
                self.bucket -= 1
                return True, 0
            return False, (1 -  self.bucket) / self.rate

    def acquire(self):
        """Blocking acquire.

        Calls `try_acquire` in a loop until successful.
        """
        while True:
            done, sleep_sec = self.try_acquire()
            if done:
                return
            time.sleep(sleep_sec)
