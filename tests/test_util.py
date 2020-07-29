from opentrons_functions.util import odd_or_even


def test_odd_or_even():

    well_name = 'A1'

    exp = 1

    obs = odd_or_even(well_name)

    assert exp == obs
