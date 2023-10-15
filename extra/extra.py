KM_LATITUDE = 1/113
KM_LONGITUDE = 1/111


def count_near_1(latitude: float, longitude: float):
    latitude1, longitude1 = (latitude - KM_LATITUDE * 1), (latitude - KM_LONGITUDE * 1)
    latitude2, longitude2 = (latitude + KM_LATITUDE * 1), (latitude + KM_LONGITUDE * 1)
    return latitude1, longitude1, latitude2, longitude2


def count_near_3(latitude: float, longitude: float):
    latitude1, longitude1 = (latitude - KM_LATITUDE * 3), (latitude - KM_LONGITUDE * 3)
    latitude2, longitude2 = (latitude + KM_LATITUDE * 3), (latitude + KM_LONGITUDE * 3)
    return latitude1, longitude1, latitude2, longitude2
