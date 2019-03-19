# -*- coding: utf-8 -*-


def fence_format(fence):
    """
    格式化经纬度坐标
    lon1,lat1,lon2,lat2…… to [[lon1,lat1],[lon2,lat2]……]
    :param fence:
    :return:
    """
    points = []
    fence_list = fence.split(",")
    for i in range(len(fence_list))[::2]:
        points.append([float(fence_list[i]), float(fence_list[i+1])])
    return points


def point_in_fence(x, y, points):
    """
    计算点是否在围栏内
    :param x: 经度
    :param y: 纬度
    :param points:  格式[[lon1,lat1],[lon2,lat2]……]
    :return:
    """
    count = 0
    x1, y1 = points[0]
    x1_part = (y1 > y) or ((x1 - x > 0) and (y1 == y))  # x1在哪一部分中
    points.append((x1, y1))
    for point in points[1:]:
        x2, y2 = point
        x2_part = (y2 > y) or ((x2 > x) and (y2 == y))  # x2在哪一部分中
        if x2_part == x1_part:
            x1, y1 = x2, y2
            continue
        mul = (x1 - x) * (y2 - y) - (x2 - x) * (y1 - y)
        if mul > 0:  # 叉积大于0 逆时针
            count += 1
        elif mul < 0:
            count -= 1
        x1, y1 = x2, y2
        x1_part = x2_part
    if count == 2 or count == -2:
        return True
    else:
        return False
