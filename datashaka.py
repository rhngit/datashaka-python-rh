import requests


class DataShaka(object):

    def __init__(self, token, groupspace):
        self.token = token
        self.groupspace = groupspace
        self.base_url = "https://api.datashaka.com/v1/"
        self.headers = {"context-type": "application/json"}

    def generate_url(self, endpoint="discovery", format=".json"):
        """Generates standard URL format for POST requests
        """
        return self.base_url + endpoint + format + "?token=" +  self.token + "&groupspace=" + self.groupspace

    def discover(self, data="", endpoint="discovery", format=".json"):
        """Builds generic POST request with data
        See https://github.com/DataShaka/datashaka-api/blob/master/routes/discovery.md

        Args:
            data: the payload for the request
            endpoint: which endpoint to POST to
            format: .json

        Returns:
            JSON formatted result
        """
        request_url = self.generate_url(endpoint, format)

        r = requests.post(request_url, json=data, headers=self.headers)
        return r.json()

    def upsert(self, data="", format=".json"):
        """Upsert data to groupspace
        https://github.com/DataShaka/datashaka-api/blob/master/routes/upsert.md

        Use format to control whether JTCSV or TCSV are to be handled
        Returns Success or Failure message

        Args:
            data: Either JTCSV or TSCV (text) formatted data
            format: .json or .tcsv

        Returns:
            IsSuccess : true or false
            Warning : typically, when the data document is empty
            Error : Upsert didnt complete and the data is not in live

        Example:
            api = DataShaka(DATASHAKA_TOKEN, DATASHAKA_GROUPSPACE)
            res = api.upsert(data=data)
        """
        headers = self.headers
        if format == ".tcsv":
            headers = {"context-type": "text/plain"}

        request_url = self.generate_url("upsert", format=format)

        r = requests.post(request_url, json=data, headers=headers)
        return r.json()

    def retrieve(self, data="", format=".json"):
        """The Retrieve route allows you to query and/or manipulate stored data from a given groupspace
        https://github.com/DataShaka/datashaka-api/blob/master/routes/retrieve.md

        Args:
            data: A dictionary of parameters
            format: Format of the output (.json, .tcsv, .csv, .html)

        Returns:
            Result formatted according to format parameter

        Example:
            api = DataShaka(DATASHAKA_TOKEN, DATASHAKA_GROUPSPACE)
            q = api.build_retrieve(time_from="2016-01-01", time_to="2016-01-07",
                       signal="{Sales}", context="[Country]",
                       tractor="crop [Country] ~> sort by time ~> group by day ~> sum")
            res = api.retrieve(data=q, format=".csv")
        """
        request_url = self.generate_url(endpoint="retrieve", format=format)
        r = requests.post(request_url, json=data, headers=self.headers)
        if format == ".json":
            return r.json()
        else:
            return r.text

    def build_retrieve(self, time_from, time_to, signal, context, tractor, tractors=[]):
        """Build a dictionary of parameters to post to the retrieve endpoint

        Args:
            time_from: ISO8601 conform timestamp (optional)
            time_to: ISO8601 conform timestamp (optional)
            signal: List of signals, each enclosed in braces {} (optional)
            context: List of contexts, each enclosed in square brackets (optional)
            tractor: A Tractor script to be executed post-query and after tractors have returned data (optional)
            tractors: An array of Tractor script to be executed post-query in parallel (optional)

        Returns:
            Dictionary of non-empty arguments

        Example:
            api = DataShaka(DATASHAKA_TOKEN, DATASHAKA_GROUPSPACE)
            q = api.build_retrieve(time_from="2016-01-01", time_to="2016-01-07",
                       signal="{Sales}", context="[Country]",
                       tractor="crop [Country] ~> sort by time ~> group by day ~> sum")
        """
        res = dict()
        res['time_from'] = time_from
        res['time_to'] = time_to
        res['signal'] = signal
        res['context'] = context
        res['tractor'] = tractor
        if len(tractors) > 0:
            res['tractors'] = []
            for t in tractors:
                res['tractors'].append(t)

        res = {k:v for k,v in res.items() if v is not None}
        res = {k:v for k,v in res.items() if v != ""}

        return res

    # Simple wrappers for specific discover types
    def discover_time(self, data, format):
        return self.discover(data=data, endpoint="discover/time", format=format)

    def discover_context(self, data, format):
        return self.discover(data=data, endpoint="discover/context", format=format)

    def discover_signal(self, data, format):
        return self.discover(data=data, endpoint="discover/signal", format=format)

    def discover_shape(self, data, format):
        return self.discover(data=data, endpoint="discover/shape", format=format)

    def discover_groupspace(self, data, format):
        return self.discover(data=data, endpoint="discover/groupspace", format=format)
