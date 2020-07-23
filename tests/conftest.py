import pytest

@pytest.fixture(scope="module")
def protocol_setup(imports, labware, payload, 
                   author='test',
                   api_version=(2, 5)):

    labware_str = "\n    ".join(labware)
    protocol_str = ("from opentrons import protocol_api\n"
                    "{imports}\n"
                    "\n"
                    "metadata = {\n"
                    "            'apiLevel': '{api0}.{api11}',\n"
                    "            'author': '{author}'}\n"
                    "\n"
                    "def run(protocol: protocol_api.ProtocolContext):\n"
                    "    {labware_str}\n"
                    "    {payload}\n")


@pytest.fixture(scope="module")
def deck(name, definition, position):
    out = ("{0} = protocol.load_labware('{1}', {2})".format(
            name, definition, position))
    
    return([out])

@pytest.fixture(scope="module")
def magblock(name, definition, position):
    block = ("magblock = protocol.load_module("
             "'Magnetic Module', {0})".format(position))
    plate = ("{0} = magblock.load_labware('{1}')".format(
              name, definition))

    return([block, plate])
                                     