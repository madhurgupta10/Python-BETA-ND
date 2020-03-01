from collections import namedtuple
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath

import operator
import collections


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple(
        'Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """

        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)
        self.date = kwargs.get('date', None)
        self.number = kwargs.get('number', None)
        self.filter = kwargs.get('filter', None)
        self.return_object = kwargs.get('return_object', None)

        # TODO: What instance variables will be useful for storing on the Query object?

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        filters = list()

        object_to_return = Query.ReturnObjects.get(self.return_object)
        search_date = Query.DateSearch(DateSearch.equals.name, self.date) if self.date else Query.DateSearch(
            DateSearch.between.name, [self.start_date, self.end_date])

        if self.filter is not None:
            options = Filter.create_filter_options(self.filter)

            for key, value in options.items():
                for a_f in value:
                    option = a_f.split(':')[0]
                    operation = a_f.split(':')[1]
                    value = a_f.split(':')[-1]
                    filters.append(Filter(option, key, operation, value))

        return Query.Selectors(search_date, self.number, filters, object_to_return)

        # TODO: Translate the query parameters into a QueryBuild.Selectors object


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        'diameter': 'diameter_min_km',
        'distance': 'miss_distance_kilometers',
        'is_hazardous': 'is_potentially_hazardous_asteroid'
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
    }

    Operators = {
        '>=': operator.ge,
        '=': operator.eq,
        '>': operator.gt
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        output = collections.defaultdict((list))

        for f in filter_options:
            afilter = f.split(':')[0]

            if hasattr(NearEarthObject(), Filter.Options.get(afilter)):
                output['NearEarthObject'].append(f)
            else:
                if hasattr(OrbitPath(), Filter.Options.get(afilter)):
                    output['OrbitPath'].append(f)

        return output

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """

        output = list()

        for my_object in results:
            field = Filter.Options.get(self.field)
            value = getattr(my_object, field)
            operation = Filter.Operators.get(self.operation)

            try:
                if not operation(value, self.value):
                    pass
                else:
                    output.append(my_object)
            except:
                if not operation(str(value), str(self.value)):
                    pass
                else:
                    output.append(my_object)
        return output

        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        self.date_search_type = None
        self.path_date_map = dict(db.path_date_map)
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors

        self.date_search_type = query.date_search.type
        date = query.date_search.values
        output = list()

        if DateSearch.equals.name == self.date_search_type:
            temp = list()
            for key, value in self.path_date_map.items():
                if key == date:
                    temp += value
            output = temp

        else:
            if DateSearch.between.name == self.date_search_type:

                temp = list()
                for key, value in self.path_date_map.items():
                    if key >= date[0] and key <= date[1]:
                        temp += value
                output = temp

        distance_filter = None
        for afilter in query.filters:
            if 'distance' == afilter.field:
                distance_filter = afilter
                continue
            else:
                pass
            output = afilter.apply(output)

        temp = list()
        for n in output:
            temp += n.orbits
        orbits = temp

        filtered_orbits = orbits
        filtered_neos = output

        if distance_filter is not None:
            filtered_neos = [self.db.neo_name_map.get(
                path.neo_name) for path in distance_filter.apply(orbits)]

        filtered_orbits = list(set(filtered_orbits))
        filtered_neos = list(set(filtered_neos))

        if OrbitPath == query.return_object:
            return filtered_orbits[: int(query.number)]
        return filtered_neos[: int(query.number)]
