import pytest
import logging
from opentrons import simulate
from opentrons.simulate import get_protocol_api, CommandScraper
from opentrons_functions.magbeads import *

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
           'Mixing 5 times with a volume of 200.0 ul',
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

    cols = ['A1','A2']
    
    bead_mix(pipette,
             plate,
             cols,
             tips)

    exp = ['Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Mixing 5 times with a volume of 200.0 ul',
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
           'Mixing 5 times with a volume of 200.0 ul',
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
