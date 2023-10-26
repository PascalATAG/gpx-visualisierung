import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

def speed_and_distance(detailed_coordinates):
    try:
        total_distance = 0.0
        total_time = 0.0
        max_speed = 0.0

        for i in range(len(detailed_coordinates) - 1):
            lat1, lon1, time1, ele1 = detailed_coordinates[i]
            lat2, lon2, time2, ele2 = detailed_coordinates[i + 1]

            distance = haversine(lat1, lon1, lat2, lon2)

            time_elapsed = (time2 - time1).total_seconds() / 3600.0

            if time_elapsed > 0:
                speed = distance / time_elapsed
                max_speed = max(max_speed, speed)

            total_distance += distance
            total_time += time_elapsed

        average_speed = total_distance / total_time

        return round(average_speed, 2), round(total_distance, 2), round(max_speed, 2)
    except:
        return False

def elevation(detailed_coordinates):
    try:
        total_elevation = 0.0
        max_elevation = 0.0

        for i in range(len(detailed_coordinates)):
            ele = detailed_coordinates[i][3]
            total_elevation += ele

            max_elevation = max(max_elevation, ele)
        
        average_elevation = total_elevation / len(detailed_coordinates)
        
        return round(average_elevation, 2), round(max_elevation, 2)
    except:
        return False