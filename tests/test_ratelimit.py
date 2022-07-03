#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

from diseaz.algo import ratelimit


class TimerStub:
    def __init__(self, now):
        self.now = now

    def time(self):
        return self.now


def test_burst():
    timer = TimerStub(1)
    rl = ratelimit.RateLimiter(2, 2, timefunc=timer.time)
    assert [rl.try_acquire() for _ in range(3)] == [(True, 0), (True, 0), (False, 0.5)]


def test_initial_burst():
    timer = TimerStub(1)
    rl = ratelimit.RateLimiter(2, 1, timefunc=timer.time)
    assert [rl.try_acquire() for _ in range(3)] == [(True, 0), (False, 0.5), (False, 0.5)]


def test_negative_initial_burst():
    timer = TimerStub(1)
    rl = ratelimit.RateLimiter(2, 2, initial_burst=-1, timefunc=timer.time)
    assert rl.try_acquire() == (False, 1)

    timer.now += 1
    assert rl.try_acquire() == (True, 0)
    assert rl.try_acquire() == (False, 0.5)


def test_small_steps():
    timer = TimerStub(1)
    rl = ratelimit.RateLimiter(2, 2, initial_burst=0, timefunc=timer.time)

    result = []
    for _ in range(5):
        timer.now += 0.15
        r, s = rl.try_acquire()
        result.append((r, round(s, 6)))
    assert result == [(False, 0.35), (False, 0.2), (False, 0.05), (True, 0), (False, 0.25)]
