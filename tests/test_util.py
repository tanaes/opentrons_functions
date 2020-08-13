from opentrons_functions.util import (odd_or_even)


def test_odd_or_even():
    exp = 1
    obs = odd_or_even('A1')

    assert exp == obs

    exp = 0
    obs = odd_or_even('A12')

    assert exp == obs
