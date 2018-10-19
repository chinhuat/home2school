#!/usr/bin/env python

import math


"""
A data model for encapsulating location name, x, y coordinate and other
connected locations.
"""
class Location:

    name = None 
    x = 0
    y = 0
    connectedLocations = []


    def __init__(self, name, x, y):

        self.name = name
        self.x = x
        self.y = y
        self.connectedLocations = []


    def getName(self):
    
        return self.name


    """ Add a connected location """
    def connectTo(self, location):

        self.connectedLocations.append(location)


    """ Return all connected locations """
    def getConnectedLocations(self):

        return self.connectedLocations


    """ Calculate distance to another location """
    def distanceTo(self, location):
    
        return math.sqrt(pow(self.x - location.x, 2) + pow(self.y - location.y, 2))


    """ Overload for printing convenience """
    def __str__(self):

        if len(self.connectedLocations) > 0:
            """ Fancy way to join name of all locations into one-liner """
            connectedLocationNames = reduce(lambda a, b: a + ", " + b, map(lambda a: a.getName(), self.connectedLocations))
            return "{} ({}, {}) is connected to {}".format(self.name, self.x, self.y, connectedLocationNames)
        else:
            return "{} ({}, {})".format(self.name, self.x, self.y)




"""
A path is collection of locations
"""
class Path:

    locations = []


    def __init__(self):
        self.locations = []


    """ Add next location """
    def addLocation(self, location):

        """ Sanity check to make sure the next location is connected to the last known location """
        if len(self.locations) > 0:
            lastLocationIndex = len(self.locations) - 1
            lastLocation = self.locations[lastLocationIndex]
            assert location in lastLocation.getConnectedLocations(), "Can't add {} to path as {} is not connected to {}".format(location.getName(), lastLocation.getName(), location.getName())

        self.locations.append(location)


    def getDistance(self):

        d = 0

        pathSegments = len(self.locations) - 1;

        """ Accumulate distances between two locations along the path """
        for i in range(pathSegments):
            d += self.locations[i].distanceTo(self.locations[i + 1])

        return d


    """ Overload for printing convenience """
    def __str__(self):
        s = ""
        
        for i in range(len(self.locations)):
            s += self.locations[i].getName()
            if i < len(self.locations) - 1:
                s += " -> "
            else:
                s += " = {:.2f}".format(self.getDistance())
        return s



"""
A walker which traverses all connected locations recursively to compute a list
of unique paths
"""
class Walker:

    previousWalker = None
    startLocation = None
    
    """ Previous walker is not required for root walker object """
    def __init__(self, startLocation, previousWalker=None):

        self.startLocation = startLocation
        self.previousWalker = previousWalker


    def getPreviousWalker(self):
        return self.previousWalker


    def getLocation(self):
        return self.startLocation


    """ Return true if the location has been visited by current or parent walkers """
    def isVisited(self, location):

        if self.getLocation() == location:
            return True
        else:
            if self.getPreviousWalker() == None:
                return False
            else:
                return self.getPreviousWalker().isVisited(location)


    def walk(self, endLocation):

        paths = []

        self._fanout(paths, endLocation)

        return paths


    """ A fan-out recursively to discovery unique paths """
    def _fanout(self, paths, endLocation):

        if self.startLocation == endLocation:

            """ Create a path if we've reached the end location """

            locations = []
            locations.append(self.startLocation)

            previousWalker = self.previousWalker

            while previousWalker != None:
                locations.append(previousWalker.getLocation())
                previousWalker = previousWalker.getPreviousWalker()
            
            path = Path()

            for location in reversed(locations):
                path.addLocation(location)

            paths.append(path)

        else:

            """ recursively fan-out to visit all connected locations """
            for connectedLocation in self.startLocation.getConnectedLocations():

                """ Do not revisit a location that's been visited to avoid infinite loop """
                if not self.isVisited(connectedLocation):

                    """
                    Create new instance of walker chaining to the current one
                    and continue to fan-out recursively
                    """
                    Walker(connectedLocation, self)._fanout(paths, endLocation)




def main():

    """ Setup locations """
    home = Location("Home", 10, 10)
    shop = Location("Shop", 10, 20)
    park = Location("Park", 20, 20)
    library = Location("Library", 25, 10)
    school = Location("School", 30, 20)

    locations = [ home, shop, park, library, school ]


    """ Setup connection between locations """
    home.connectTo(shop)
    home.connectTo(park)
    home.connectTo(library)
    shop.connectTo(park)
    park.connectTo(school)
    park.connectTo(home)
    park.connectTo(library)
    library.connectTo(park)
    library.connectTo(school)


    for location in locations:
        print str(location)
        
    print


    for location in locations:
        for connectedLocation in location.getConnectedLocations():
            print "{} to {} distance is {:.2f}".format(location.getName(), connectedLocation.getName(), location.distanceTo(connectedLocation))

    print

    """
    Get all possible paths from home to school, the walk method is implemented
    using composite pattern (https://en.wikipedia.org/wiki/Composite_pattern)
    which would fan-out recursively to traverse non-overlapping paths.
    """    
    paths = Walker(home).walk(school)

    """ sort paths using lambda expression, shortest distance first """
    sortedPaths = sorted(paths, key=lambda p: p.getDistance())
    
    for sortedPath in sortedPaths:
        print str(sortedPath)


if __name__ == "__main__":
    main()
