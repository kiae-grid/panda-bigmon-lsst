#!/usr/bin/env python
#
# Class that measures elapsed time and can be used to
# get timing profile for various pieces of code.

import time

class ProfilingTimer(object):
    """
    Implements timer that measures time between multiple
    start/stop events summing up the result.
    """

    def __init__(self, description):
        """ Description should give an idea about this timer's purpose """
        self._description = description
        self.reset()


    def start(self):
        """ Makes timer to start ticking """
        self._start = time.time()


    def stop(self):
        """ Stops the timer """
        self._stop = time.time()
        self._cumulative += (self._stop - self._start)


    def reset(self):
        """ Resets everything """
        self._start = 0
        self._end = 0
        self._cumulative = 0


    def get_description(self):
        """ Returns timer description """
        return self._description


    def get_elapsed(self):
        """ Returns elapsed time """
        return self._cumulative


    def __repr__(self):
        return "%s: %ss" % (self._description, self._cumulative)


if __name__ == "__main__":
    import unittest
    import random

    class ProfilingTimerTests(unittest.TestCase):

        def __init__(self, methodName):
            """ Sets up instance """
            self.timer_name = "Our profiling timer"
            random.seed()
            self.timer_sleeptime = random.random()
            self.timer_inst = ProfilingTimer(self.timer_name)
            super(ProfilingTimerTests, self).__init__(methodName)

        def test_timer_init(self):
            self.assertEqual(self.timer_inst.get_description(),
              self.timer_name)

        def test_timer_just_started(self):
            self.timer_inst.reset()
            self.timer_inst.start()
            self.assertEqual(self.timer_inst.get_elapsed(), 0)

        def test_timer_reset(self):
            self.timer_inst.start()
            time.sleep(self.timer_sleeptime)
            self.timer_inst.stop()
            self.timer_inst.reset()
            self.assertEqual(self.timer_inst.get_elapsed(), 0)

        def test_timer(self):
            self.timer_inst.reset()
            self.timer_inst.start()
            time.sleep(self.timer_sleeptime)
            self.timer_inst.stop()
            self.assertTrue(self.timer_inst.get_elapsed() >= 0)

        def test_timer_cumulativity(self):
            self.timer_inst.reset()
            self.timer_inst.start()
            time.sleep(self.timer_sleeptime)
            self.timer_inst.stop()
            dt = self.timer_inst.get_elapsed()
            self.timer_inst.start()
            time.sleep(self.timer_sleeptime)
            self.timer_inst.stop()
            self.assertTrue(self.timer_inst.get_elapsed() >= 0)
            self.assertTrue(self.timer_inst.get_elapsed() >= dt)

    unittest.main()
