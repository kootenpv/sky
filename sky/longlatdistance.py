import math
 
def lat_long_distance(lat1, long1, lat2, long2):

    degrees_to_radians = math.pi/180.0
         
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians 
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    return arc * 6373

lat_long_distance(52.080318, 4.854670, 52.097999, 4.328490)

