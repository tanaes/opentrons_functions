import pytest
import logging
from opentrons.simulate import get_protocol_api, CommandScraper
from opentrons_functions.transfer import (add_buffer,
                                          get_96_from_384_wells)

apilevel = '2.5'


def test_add_buffer():
    protocol = get_protocol_api(apilevel)
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    reagents = protocol.load_labware('nest_12_reservoir_15ml',
                                     9, 'reagents')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    remaining, source_wells = add_buffer(pipette,
                                         [reagents['A1']],
                                         plate,
                                         ['A1', 'A2'],
                                         300,
                                         1000)

    assert remaining == 400
    assert source_wells == [reagents['A1']]

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A1 of plate on 3 at 1.0 speed',
           'Blowing out',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A2 of plate on 3 at 1.0 speed',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A2 of plate on 3 at 1.0 speed',
           'Blowing out',
           'Dropping tip into A1 of Opentrons Fixed Trash on 12']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_add_buffer_runout():
    protocol = get_protocol_api(apilevel)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    reagents = protocol.load_labware('nest_12_reservoir_15ml',
                                     9, 'reagents')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    with pytest.raises(IndexError):
        remaining, source_wells = add_buffer(pipette,
                                             [reagents['A1']],
                                             plate,
                                             ['A1', 'A2'],
                                             300,
                                             600)


def test_add_buffer_fullplate():
    protocol = get_protocol_api(apilevel)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    reagents = protocol.load_labware('usascientific_12_reservoir_22ml',
                                     9, 'reagents')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    remaining, source_wells = add_buffer(pipette,
                                         [reagents['A1'],
                                          reagents['A2']],
                                         plate,
                                         ['A1', 'A2', 'A3', 'A4',
                                          'A5', 'A6', 'A7', 'A8',
                                          'A9', 'A10', 'A11', 'A12'],
                                         300,
                                         20000 / 8,
                                         dead_vol=800 / 8)

    assert remaining == 1300
    assert source_wells == [reagents['A2']]


def test_add_buffer_even():
    protocol = get_protocol_api(apilevel)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    reagents = protocol.load_labware('usascientific_12_reservoir_22ml',
                                     9, 'reagents')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    remaining, source_wells = add_buffer(pipette,
                                         [reagents['A1'],
                                          reagents['A2']],
                                         plate,
                                         ['A1', 'A2', 'A3', 'A4',
                                          'A5', 'A6', 'A7', 'A8'],
                                         25,
                                         200,
                                         dead_vol=100)

    assert remaining == 100
    assert source_wells == [reagents['A2']]


def test_add_buffer_touch_tip():
    protocol = get_protocol_api(apilevel)
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    reagents = protocol.load_labware('nest_12_reservoir_15ml',
                                     9, 'reagents')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    remaining, source_wells = add_buffer(pipette,
                                         [reagents['A1']],
                                         plate,
                                         ['A1', 'A2'],
                                         300,
                                         1000,
                                         touch_tip=True)

    assert remaining == 400
    assert source_wells == [reagents['A1']]

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A1 of plate on 3 at 1.0 speed',
           'Touching tip',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A1 of plate on 3 at 1.0 speed',
           'Touching tip',
           'Blowing out',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A2 of plate on 3 at 1.0 speed',
           'Touching tip',
           'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
           'Dispensing 160.0 uL into A2 of plate on 3 at 1.0 speed',
           'Touching tip',
           'Blowing out',
           'Dropping tip into A1 of Opentrons Fixed Trash on 12']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_get_96_from_384_wells_interleaved():
    a = [x for x in get_96_from_384_wells(method='interleaved', start=1)][0:3]
    b = [x for x in get_96_from_384_wells(method='interleaved', start=2)][0:3]
    c = [x for x in get_96_from_384_wells(method='interleaved', start=3)][0:3]
    d = [x for x in get_96_from_384_wells(method='interleaved', start=4)][0:3]

    assert a == ['A1', 'C1', 'E1']
    assert b == ['B1', 'D1', 'F1']
    assert c == ['A2', 'C2', 'E2']
    assert d == ['B2', 'D2', 'F2']


def test_get_96_from_384_wells_packed():
    a = [x for x in get_96_from_384_wells(method='packed', start=1)][0:3]
    b = [x for x in get_96_from_384_wells(method='packed', start=2)][0:3]
    c = [x for x in get_96_from_384_wells(method='packed', start=3)][0:3]
    d = [x for x in get_96_from_384_wells(method='packed', start=4)][0:3]

    assert a == ['A1', 'C1', 'E1']
    assert b == ['A7', 'C7', 'E7']
    assert c == ['A13', 'C13', 'E13']
    assert d == ['A19', 'C19', 'E19']
