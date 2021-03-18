import Constants


# Scales a set of coordinates to the current screen size based on a divisor factor
def cscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([int(coordinate[x] / divisor * Constants.SCREEN_SIZE[x % 2]) for x in range(len(coordinate))])
    else:
        return int(coordinate[0] / divisor * Constants.SCREEN_SIZE[0])


# Scales a set of coordinates to the current screen size based on a divisor factor. Doesn't return integers
def posscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([coordinate[x] / divisor * Constants.SCREEN_SIZE[x] for x in range(len(coordinate))])
    else:
        return coordinate[0] / divisor * Constants.SCREEN_SIZE[0]
