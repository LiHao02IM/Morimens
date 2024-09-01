import get_location

region = (1600, 750, 300, 120)


# 没有费用时返回next地址，还有费用则返回空
def way1():
    location = get_location.way3('next1.png', region)
    if location is not None:
        return location
    else:
        return None


# 出牌数达到上限,强制进入下一回合，返回next地址，无法进入下一回合则返回空
def way2():
    location = get_location.way3('next1.png', region)
    if location is None:
        location = get_location.way3('next2.png', region)
        if location is None:
            location = get_location.way3('next3.png', region)
            if location is None:
                return None
    return location
