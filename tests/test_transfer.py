import pytest
import logging
from opentrons import simulate
from opentrons.simulate import get_protocol_api, CommandScraper
from opentrons_functions.transfer import *

def test_example():
    exp = 1
    obs = example()

    assert exp==obs

def test_simple_transfer():
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

    simple_transfer(pipette,
                    plate['A1'],
                    plate['A2'],
                    vol=100)

    exp = ['Transferring 100.0 from A1 of plate on 3 to A2 of plate on 3',
           'Picking up tip from A1 of Opentrons 96 Tip Rack 300 µL on 8',
           'Aspirating 100.0 uL from A1 of plate on 3 at 1.0 speed',
           'Dispensing 100.0 uL into A2 of plate on 3 at 1.0 speed',
           'Dropping tip into A1 of Opentrons Fixed Trash on 12']

    obs = [x['payload']['text'] for x in scraper.commands]

    assert exp == obs