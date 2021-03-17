import pytest
import logging

from opentrons.simulate import get_protocol_api, CommandScraper
from opentrons_functions.magbeads import (bead_mix, remove_supernatant,
                                          bead_wash, transfer_elute)


def test_bead_mix():
    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1']

    bead_mix(pipette,
             plate,
             cols,
             tips)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Blowing out at A1 of plate on 3',
           'Returning tip',
           'Dropping tip into A1 of Opentrons 96 Tip Rack 300 µL on 8']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_bead_mix_lift():
    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1']

    bead_mix(pipette,
             plate,
             cols,
             tips,
             mix_lift=10)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Blowing out at A1 of plate on 3',
           'Returning tip',
           'Dropping tip into A1 of Opentrons 96 Tip Rack 300 µL on 8']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_bead_mix_2cols():
    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1', 'A2']

    bead_mix(pipette,
             plate,
             cols,
             tips)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of plate on 3 at 1.0 speed',
           'Blowing out at A1 of plate on 3',
           'Returning tip',
           'Dropping tip into A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Picking up tip from A2 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 200.0 uL from A2 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A2 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A2 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A2 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A2 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A2 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A2 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A2 of plate on 3 at 1.0 speed',
           'Aspirating 200.0 uL from A2 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A2 of plate on 3 at 1.0 speed',
           'Blowing out at A2 of plate on 3',
           'Returning tip',
           'Dropping tip into A2 of Opentrons 96 Tip Rack 300 µL on 8']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_remove_supernatant():
    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    waste = protocol.load_labware('nest_1_reservoir_195ml',
                                  7, 'waste')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1']

    remove_supernatant(pipette,
                       plate,
                       cols,
                       tips,
                       waste['A1'],
                       super_vol=200,
                       tip_vol=200,
                       rate=0.25,
                       bottom_offset=2,
                       drop_tip=False)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 190.0 uL from A1 of plate on 3 at 0.25 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 200.0 uL into A1 of waste on 7 at 1.0 speed',
           'Aspirating 10.0 uL from A1 of plate on 3 at 0.25 speed',
           'Air gap',
           'Aspirating 10.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 20.0 uL into A1 of waste on 7 at 1.0 speed',
           'Blowing out',
           'Returning tip',
           'Dropping tip into A1 of Opentrons 96 Tip Rack 300 µL on 8']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_bead_wash():
    apilevel = '2.5'
    protocol = get_protocol_api(apilevel)
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    reagents = protocol.load_labware('nest_12_reservoir_15ml',
                                     9, 'reagents')
    waste = protocol.load_labware('nest_1_reservoir_195ml',
                                  7, 'waste')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])
    magblock = protocol.load_module('Magnetic Module', 10)
    mag_plate = magblock.load_labware('biorad_96_wellplate_200ul_pcr')

    cols = ['A1']

    remaining, wells = bead_wash(  # global arguments
        protocol,
        magblock,
        pipette,
        mag_plate,
        cols,
        # super arguments
        waste['A1'],
        tips,
        # wash buffer arguments
        [reagents['A1']],
        20000 / 8,
        # mix arguments
        tips,
        # optional arguments
        super_vol=150,
        rate=0.25,
        super_bottom_offset=2,
        drop_super_tip=True,
        wash_vol=150,
        remaining=None,
        wash_tip=None,
        drop_wash_tip=True,
        mix_vol=200,
        mix_n=2,
        drop_mix_tip=False,
        mag_engage_height=None,
        pause_s=300
    )
    assert remaining == pytest.approx(2350.0)
    assert wells == [reagents['A1']]

    exp = [
        'Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
        'Aspirating 150.0 uL from A1 of Bio-Rad 96 Well Plate 200 µL PCR on'
        ' Magnetic Module GEN1 on 10 at 0.25 speed',
        'Air gap',
        'Aspirating 10.0 uL from A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Dispensing 160.0 uL into A1 of waste on 7 at 1.0 speed',
        'Blowing out',
        'Dropping tip into A1 of Opentrons Fixed Trash on 12',
        'Disengaging Magnetic Module',
        'Picking up tip from A2 of Opentrons 96 Tip Rack 300 µL on 8',
        'Aspirating 150.0 uL from A1 of reagents on 9 at 1.0 speed',
        'Air gap',
        'Aspirating 10.0 uL from A1 of reagents on 9 at 1.0 speed',
        'Dispensing 160.0 uL into A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Blowing out',
        'Dropping tip into A1 of Opentrons Fixed Trash on 12',
        'Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
        'Aspirating 200.0 uL from A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Dispensing 200.0 uL into A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Aspirating 200.0 uL from A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Dispensing 200.0 uL into A1 of Bio-Rad 96 Well Plate 200 µL PCR on '
        'Magnetic Module GEN1 on 10 at 1.0 speed',
        'Blowing out at A1 of Bio-Rad 96 Well Plate 200 µL PCR on Magnetic '
        'Module GEN1 on 10',
        'Returning tip',
        'Dropping tip into A1 of Opentrons 96 Tip Rack 300 µL on 8',
        'Engaging Magnetic Module',
        'Delaying for 5 minutes and 0 seconds']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_transfer_elute():

    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    elute = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  7, 'elute')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1']

    transfer_elute(pipette,
                   plate,
                   elute,
                   cols,
                   tips,
                   50,
                   z_offset=0.5,
                   x_offset=1,
                   rate=0.25,
                   drop_tip=True)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 50.0 uL from A1 of plate on 3 at 0.25 speed',
           'Dispensing 50.0 uL into A1 of elute on 7 at 1.0 speed',
           'Dropping tip into A1 of Opentrons Fixed Trash on 12']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs


def test_transfer_elute_mix():

    protocol = get_protocol_api('2.5')
    scraper = CommandScraper(logging.getLogger('opentrons'),
                             '1',
                             protocol.broker)

    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  3, 'plate')
    elute = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                  7, 'elute')
    pipette = protocol.load_instrument('p300_multi',
                                       'left',
                                       tip_racks=[tips])

    cols = ['A1']

    transfer_elute(pipette,
                   plate,
                   elute,
                   cols,
                   tips,
                   50,
                   z_offset=0.5,
                   x_offset=1,
                   rate=0.25,
                   drop_tip=True,
                   mix_n=2,
                   mix_vol=50)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 50.0 uL from A1 of plate on 3 at 0.25 speed',
           'Dispensing 50.0 uL into A1 of elute on 7 at 1.0 speed',
           'Mixing 2 times with a volume of 50.0 ul',
           'Aspirating 50.0 uL from A1 of elute on 7 at 1.0 speed',
           'Dispensing 50.0 uL into A1 of elute on 7 at 1.0 speed',
           'Aspirating 50.0 uL from A1 of elute on 7 at 1.0 speed',
           'Dispensing 50.0 uL into A1 of elute on 7 at 1.0 speed',
           'Blowing out at A1 of elute on 7',
           'Dropping tip into A1 of Opentrons Fixed Trash on 12']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs
