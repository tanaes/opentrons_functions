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
        pipette.mix(pre_mix,
                    tip_vol*.9,
                    source_well)

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
                    if pre_mix is not None:
                        pipette.mix(pre_mix,
                                    tip_vol*.9,
                                    source_well)
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


def get_96_from_384_wells(method='interleaved', start=1):
    if method == 'interleaved':
        rows = [chr(64 + x * 2 - (start % 2))
                for x in range(1, 9)]
        cols = [x * 2 - int((start + 1) / 2) % 2
                for x in range(1, 13)]

        for col in cols:
            for row in rows:
                yield('%s%s' % (row, col))

    if method == 'packed':
        for col in range((start - 1) * 6 + 1,
                         (start - 1) * 6 + 7):
            for row in [chr(x + 65) for x in range(0, 16, 2)]:
                yield('%s%s' % (row, col))
        for col in range((start - 1) * 6 + 1,
                         (start - 1) * 6 + 7):
            for row in [chr(x + 65) for x in range(1, 17, 2)]:
                yield('%s%s' % (row, col))
