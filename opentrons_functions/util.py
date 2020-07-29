def odd_or_even(well_name):
    assert type(well_name) == str
    try:
        col = int(well_name[1:])
    except IndexError:
        print("")
        raise

    return(col % 2)
