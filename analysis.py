import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance

def total_distance(coordinates):
    total = 0.0
    for i in range(len(coordinates) - 1):
        lat1, lon1 = coordinates[i]
        lat2, lon2 = coordinates[i + 1]
        total += haversine(lat1, lon1, lat2, lon2)

    return total

def speed_and_elevation_data(detailed_coordinates):
    try:
        total_distance = 0.0
        total_time = 0.0
        total_elevation = 0.0
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
            total_elevation += ele1

        total_elevation += detailed_coordinates[-1][3]
        average_elevation = total_elevation / len(detailed_coordinates)
        average_speed = total_distance / total_time

        return average_speed, average_elevation, max_speed
    except:
        return False
