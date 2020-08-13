from requests import post


def odd_or_even(well_name):
    assert type(well_name) == str
    try:
        col = int(well_name[1:])
    except IndexError:
        print("")
        raise

    return(col % 2)


def change_name(robot_ip,
                newname):
    endpoint = 'http://{robot_ip}:31950/server/name'

    r = post(endpoint.format(robot_ip=robot_ip),
             json={"name": newname})

    return(r)
