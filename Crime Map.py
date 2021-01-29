import matplotlib.pyplot as plt
import math

def loadData(filename):
    crime_data = open(filename)
    next(crime_data)
    
    coords = [line.split(',') for line in crime_data]
    crimeLocs = [(float(coord[0]), float(coord[1][:-1])) for coord in coords] 
    lat = [float(coord[0]) for coord in coords]
    long = [float(coord[1][:-1]) for coord in coords]    
    
    return (lat, long, crimeLocs) 

class Map(object):
    def __init__(self, lat, long, numZones):
        "Assumes lat and long ar lists."
        self.lat = lat
        self.long = long
        self.numZones = numZones
        self.zones = []
        self.scalar = 100000 
        self.hits = {} 
    
    def generate_zones(self):        
        latRange = self.get_lat_range()
        longRange = self.get_long_range() 
        latStep = round(len(latRange)/float(self.numZones))
        longStep = round(len(longRange)/float(self.numZones)) 
        
        for i in  range(latRange[0], latRange[-1], latStep):
            for j in range(longRange[0], longRange[-1], longStep):
                self.zones.append(((i, i + latStep), (j,j + longStep)))
       
    def get_lat_range(self):
        return range(round(self.scalar*(min(self.lat) - 0.05)), round(self.scalar*(max(self.lat) + 0.05)))
    
    def get_long_range(self):
        return range(round(self.scalar*(min(self.long) - 0.05)), round(self.scalar*(max(self.long) + 0.05)))
    
    def is_crime_in_zone(self, crimeLoc, zoneNum):
        if math.floor(self.scalar*crimeLoc[0]) in range(self.zones[zoneNum][0][0],self.zones[zoneNum][0][1]) and math.floor(self.scalar*crimeLoc[1]) in range(self.zones[zoneNum][1][0], self.zones[zoneNum][1][1]):
            if zoneNum not in self.hits.keys():
                self.hits[zoneNum] = [crimeLoc]
            else:
                self.hits[zoneNum].append(crimeLoc)
    
    def report_crimes(self, crimeLocs):
        for crimeLoc in crimeLocs:
            for zoneNum in range(self.numZones**2):
                self.is_crime_in_zone(crimeLoc, zoneNum) 
        
def style(numCrimes, mean):
    if numCrimes > 2*mean:
        return ('ro', 'High Crime Density')
    elif numCrimes > (2/3)*mean:
        return ('yo', 'Medium Crime Density')
    else:
        return ('go', 'Low Crime Density')
    
def plotCrimes(Map): 
    myMap = Map
    plt.figure('Chicago Car Crash Data')
    numCrimesList = []
    for area in myMap.hits.values():
        numCrimes = len(area)
        numCrimesList.append(numCrimes)
    mean = sum(numCrimesList)/len(numCrimesList)
    
    
    for area in myMap.hits.values():
        numCrimes = len(area)
        numCrimesList.append(numCrimes)
        styles = style(numCrimes, mean)
        lats = [coord[0] for coord in area]
        longs = [coord[1] for coord in area]
        plt.plot(longs, lats, styles[0], label = styles[1], alpha = .3)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')  
    plt.title('Chicago Car Crash Data')                
        