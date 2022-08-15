from threading import Thread, Timer
from abc import ABC, abstractmethod
import time
import logging


class ThreadCLass:
    _thread_watchdog_timeout = 0.1

    def __init__(self):
        self._watchdog_timer = None
        self._thread = None

    def __del__(self):
        self._cleanup()

    def initialize(self, thread_timeout):
        self._watchdog_timeout = thread_timeout
        self._thread_should_run = True
        self._thread = Thread(target=self._thread_wrapper, args=(), daemon=True)
        self._pet_watchdog()
        self._start_watchdog()
        print(f"Starting {self.name()} thread")
        self._thread.start()

    def _pet_watchdog(self):
        self._last_thread_time = time.monotonic()

    def _watchdog(self):
        current_time = time.monotonic()
        if current_time - self._last_thread_time > self._watchdog_timeout:
            # self._panic()
            print(f"wathchdog for {self.name()} expired")

        self._start_watchdog()

    def _start_watchdog(self):
        self._watchdog_timer = Timer(self._watchdog_timeout, self._watchdog)
        self._watchdog_timer.daemon = True
        self._watchdog_timer.start()

    def _thread_wrapper(self):
        while self._thread_should_run:
            self._thread_function()
            self._pet_watchdog()

    def _cleanup(self):
        self._thread_should_run = False

        if self._watchdog_timer is not None:
            self._watchdog_timer.cancel()

        if self._thread is not None:
            self._thread.join(timeout=self._thread_watchdog_timeout)
            self._thread = None

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _thread_function(self):
        raise NotImplementedError("Child class must implement the thread function!")

    @abstractmethod
    def _panic(self):
        raise NotImplementedError("Child class must implement the PANIC function!")
