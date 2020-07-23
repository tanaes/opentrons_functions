from opentrons import protocol_api

def example():
    return(1)

def simple_transfer(pipette,
                    source,
                    dest,
                    vol=10):
    pipette.transfer(vol,
                     source,
                     dest)

