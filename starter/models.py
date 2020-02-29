class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """

        self.orbits = list()

        self.name = kwargs.get('name', 'None')
        self.id = kwargs.get('id', None)

        self.is_hazardous = kwargs.get(
            'is_potentially_hazardous_asteroid', False)
        self.diameter_min_kilometers = float(kwargs.get(
            'estimated_diameter_min_kilometers', 0))

        # TODO: What instance variables will be useful for storing on the Near Earth Object?

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        self.orbits.append(orbit)

        # TODO: How do we connect orbits back to the Near Earth Object?

    def __repr__(self):
        return "NearEarthObject ID:"+str(self.id)+"NAME:"+str(self.name)+"ORBITS: "+str([orbit.neo_name for orbit in self.orbits])+"ORBIT_DATES:"+str([orbit.close_approach_date for orbit in self.orbits])

    def __str__(self):
        return "NearEarthObject ID:"+str(self.id)+"NAME:"+str(self.name)+"ORBITS: "+str([orbit.neo_name for orbit in self.orbits])+"ORBIT_DATES:"+str([orbit.close_approach_date for orbit in self.orbits])


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """

        self.neo_name = kwargs.get('name', 'None')
        self.close_approach_date = kwargs.get('close_approach_date', None)
        self.miss_distance_kilometers = float(
            kwargs.get('miss_distance_kilometers', 0))

        # TODO: What instance variables will be useful for storing on the Near Earth Object?
