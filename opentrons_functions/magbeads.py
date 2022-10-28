from opentrons import types
from opentrons_functions.transfer import add_buffer
from opentrons_functions.util import odd_or_even


def bead_mix(pipette,
             plate,
             cols,
             tiprack,
             n=5,
             z_offset=2,
             mix_rate=1,
             mix_vol=200,
             mix_lift=0,
             drop_tip=False):
    if tiprack is None:
        pipette.pick_up_tip()
    aspirated = False

    for col in cols:
        if tiprack is not None:
            pipette.pick_up_tip(tiprack.wells_by_name()[col])

        pipette.move_to(plate[col].top())
        if aspirated:
            pipette.dispense(20)
            aspirated=False
        for step in range(n):
            pipette.aspirate(mix_vol,
                             plate[col].bottom(z=z_offset),
                             rate=mix_rate)
            pipette.dispense(mix_vol,
                             plate[col].bottom(z=z_offset + mix_lift),
                             rate=mix_rate)

        pipette.blow_out(plate[col].top())
        pipette.touch_tip()
        pipette.aspirate(20)
        aspirated = True

        if tiprack is not None:
            if drop_tip:
                pipette.drop_tip()
            else:
                pipette.return_tip()

    if tiprack is None:
        if drop_tip:
            pipette.drop_tip()
        else:
            pipette.return_tip()
    return()


def remove_supernatant(pipette,
                       plate,
                       cols,
                       tiprack,
                       waste,
                       super_vol=600,
                       tip_vol=200,
                       rate=0.25,
                       bottom_offset=2,
                       dispense_rate=1,
                       blow_out=False,
                       drop_tip=False,
                       vol_fn=None):

    # remove supernatant
    if vol_fn is None:
        def vol_fn(x): return(4 if x > 185 else bottom_offset)

    for col in cols:
        vol_remaining = super_vol

        # transfers to remove supernatant:
        pipette.pick_up_tip(tiprack.wells_by_name()[col])

        dispense_gap = False
        while vol_remaining > 0:

            transfer_vol = min(vol_remaining, (tip_vol - 10))

            z_height = vol_fn(vol_remaining - transfer_vol)
            if z_height < bottom_offset:
                z_height = bottom_offset

            if dispense_gap:
                pipette.move_to(plate[col].top())
                pipette.dispense(10)

            pipette.aspirate(transfer_vol,
                             plate[col].bottom(z=z_height),
                             rate=rate)
            pipette.air_gap(10)
            pipette.dispense(transfer_vol + 10,
                             waste.top(),
                             rate=dispense_rate)
            pipette.aspirate(10)
            dispense_gap = True
            vol_remaining -= transfer_vol
        # we're done with these tips at this point
        if blow_out:
            pipette.blow_out()
        if drop_tip:
            pipette.drop_tip()
        else:
            pipette.return_tip()
    return()


def bead_wash(  # global arguments
              protocol,
              magblock,
              pipette,
              plate,
              cols,
                # super arguments
              super_waste,
              super_tiprack,
                # wash buffer arguments
              source_wells,
              source_vol,
                # mix arguments
              mix_tiprack,
                # optional arguments
              resuspend_beads=True,
              super_vol=600,
              rate=0.25,
              super_bottom_offset=2,
              super_tip_vol=200,
              super_blowout=False,
              drop_super_tip=True,
              vol_fn=None,
              wash_vol=300,
              remaining=None,
              wash_tip=None,
              wash_tip_vol=300,
              drop_wash_tip=True,
              touch_wash_tip=False,
              mix_vol=200,
              mix_n=10,
              mix_z_offset=2,
              mix_lift=0,
              mix_rate=1,
              drop_mix_tip=False,
              mag_engage_height=None,
              pause_s=300):
    # Wash

    # This should:
    # - pick up tip from position 7
    # - pick up 190 µL from the mag plate
    # - air gap
    # - dispense into position 11
    # - repeat x
    # - trash tip
    # - move to next column
    # - disengage magnet

    # remove supernatant
    remove_supernatant(pipette,
                       plate,
                       cols,
                       super_tiprack,
                       super_waste,
                       tip_vol=super_tip_vol,
                       super_vol=super_vol,
                       rate=rate,
                       bottom_offset=super_bottom_offset,
                       drop_tip=drop_super_tip,
                       blow_out=super_blowout,
                       vol_fn=vol_fn)

    if resuspend_beads:
        # disengage magnet
        magblock.disengage()

    # This should:
    # - Pick up tips from column 3 of location 2
    # - pick up isopropanol from position 5 column 3
    # - dispense to `cols` in mag plate
    # - pick up isopropanol from position 5 column 4
    # - dispense to `cols` in mag plate
    # - drop tips at end

    # add wash
    wash_wells, wash_remaining = add_buffer(pipette,
                                            source_wells,
                                            plate,
                                            cols,
                                            wash_vol,
                                            source_vol,
                                            tip=wash_tip,
                                            tip_vol=wash_tip_vol,
                                            remaining=remaining,
                                            drop_tip=drop_wash_tip,
                                            touch_tip=touch_wash_tip)

    # This should:
    # - grab a tip from position 8
    # - mix 5 times the corresponding well on mag plate
    # - blow out
    # - return tip
    # - do next col
    # - engage magnet

    if resuspend_beads:
        # mix
        bead_mix(pipette,
                 plate,
                 cols,
                 mix_tiprack,
                 n=mix_n,
                 mix_vol=mix_vol,
                 drop_tip=drop_mix_tip,
                 z_offset=mix_z_offset,
                 mix_lift=mix_lift,
                 mix_rate=mix_rate)

        # engage magnet
        if mag_engage_height is not None:
            magblock.engage(height_from_base=mag_engage_height)
        else:
            magblock.engage()

        protocol.delay(seconds=pause_s)

    return(wash_wells, wash_remaining)


def transfer_elute(pipette,
                   source,
                   dest,
                   cols,
                   tiprack,
                   vol,
                   z_offset=0.5,
                   x_offset=1,
                   rate=0.25,
                   drop_tip=True,
                   mix_n=None,
                   mix_vol=None):

    for col in cols:
        # determine offset
        side = odd_or_even(col)
        offset = (-1)**side * x_offset

        center_loc = source[col].bottom(z=z_offset)
        offset_loc = center_loc.move(types.Point(x=offset,
                                                 y=0,
                                                 z=0))

        pipette.pick_up_tip(tiprack[col])
        pipette.aspirate(vol, offset_loc, rate=rate)
        pipette.dispense(vol, dest[col])

        if mix_n is not None:
            pipette.mix(mix_n,
                        mix_vol,
                        dest[col].bottom(z=1))
            pipette.blow_out(dest[col].top())
        if drop_tip:
            pipette.drop_tip()
        else:
            pipette.return_tip()
