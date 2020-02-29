from models import OrbitPath, NearEarthObject
import csv


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """

        self.path_date_map = dict()

        self.neo_name_map = dict()

        self.filename = filename

        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        with open(filename, mode='r') as csv_file:

            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:

                my_path = OrbitPath(**row)

                if self.neo_name_map.get(row['name']):
                    pass
                else:
                    self.neo_name_map[row['name']] = NearEarthObject(**row)

                my_object = self.neo_name_map.get(row['name'])
                my_object.update_orbits(my_path)

                if self.path_date_map.get(row['close_approach_date']):
                    pass
                else:
                    self.path_date_map[row['close_approach_date']] = list()

                self.path_date_map[row['close_approach_date']].append(
                    my_object)

        return None
