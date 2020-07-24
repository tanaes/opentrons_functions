from numpy import ceil

def bead_mix(pipette,
             plate,
             cols,
             tiprack,
             n=5,
             z_offset=2,
             mix_vol=200,
             drop_tip=False):
    for col in cols:
        pipette.pick_up_tip(tiprack.wells_by_name()[col])
        pipette.mix(n, 
                    mix_vol,
                    plate[col].bottom(z=z_offset))
        pipette.blow_out(plate[col].top())

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
                       drop_tip=False):

    # remove supernatant
    
    for col in cols:
        vol_remaining = super_vol
        # transfers to remove supernatant:
        pipette.pick_up_tip(tiprack.wells_by_name()[col])
        transfers = int(ceil(super_vol/(tip_vol-10)))
        while vol_remaining > 0:
            transfer_vol = min(vol_remaining, (tip_vol-10))
            if vol_remaining <= 190:
                z_height = bottom_offset
            else:
                z_height = 4
            pipette.aspirate(transfer_vol,
                             plate[col].bottom(z=z_height),
                             rate=rate)
            pipette.air_gap(10)
            pipette.dispense(transfer_vol + 10, waste.top())
            vol_remaining -= transfer_vol
        # we're done with these tips at this point
        pipette.blow_out()
        if drop_tip:
            pipette.drop_tip()
        else:
            pipette.return_tip() 
    return()