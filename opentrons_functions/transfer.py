from numpy import ceil


def add_buffer(pipette,
               source_wells,
               dest,
               cols,
               vol,
               source_vol,
               tip=None,
               tip_vol=300,
               remaining=None,
               drop_tip=True,
               pre_mix=None,
               dead_vol=1000 / 8):

    if tip is not None:
        pipette.pick_up_tip(tip)
    else:
        pipette.pick_up_tip()

    source_well = source_wells[0]
    if remaining is None:
        remaining = source_vol

    transfers = int(ceil(vol / (tip_vol - 10)))
    transfer_vol = vol / transfers

    if pre_mix is not None:
        for well in source_wells:
            pipette.mix(pre_mix,
                        tip_vol*.9,
                        well)

    for col in cols:
        for i in range(0, transfers):
            pipette.aspirate(transfer_vol,
                             source_well)
            pipette.air_gap(10)
            pipette.dispense(transfer_vol + 10,
                             dest[col].top())

            remaining -= transfer_vol

            if remaining < transfer_vol + dead_vol:
                source_wells.pop(0)
                try:
                    source_well = source_wells[0]
                except IndexError:
                    print('Ran out of source wells!')
                    raise
                remaining = source_vol

        pipette.blow_out()

    if drop_tip:
        pipette.drop_tip()
    else:
        pipette.return_tip()

    return(remaining, source_wells)
