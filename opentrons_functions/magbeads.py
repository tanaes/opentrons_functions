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
