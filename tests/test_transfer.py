import pytest
import logging
from opentrons import simulate
from opentrons.simulate import get_protocol_api, CommandScraper
from opentrons_functions.transfer import *

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
                                         ['A1','A2'],
                                         300,               
                                         1000)

    assert remaining == 400
    assert source_wells == [reagents['A1']]
