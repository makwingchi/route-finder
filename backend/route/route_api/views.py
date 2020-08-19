from django.db import connection
from django.http import JsonResponse
from geopy.geocoders import MapBox
from rest_framework.views import APIView


class RoutesDetail(APIView):
    def get(self, request):
        """
        Respond to the get requests from the frontend

        Args:
            request (django.http.request): request from the frontend, which includes hour, origin and destination params

        Returns:
            JsonReponse (django.http.JsonResponse): GeoJson object of the shortest (safest) path (the path with fewest crashes)
        """
        query_dict = request.query_params

        # get parameters from request
        hour = int(query_dict.get("hour"))
        origin = query_dict.get("origin")
        dest = query_dict.get("destination")

        # geocode origin and destination
        api_key = "pk.eyJ1Ijoib3Blbi1hZGRyZXNzZXMiLCJhIjoiSGx0a1B1NCJ9.2O1QelK6jnFXfDznC2pNSw"
        geocoder = MapBox(api_key=api_key, timeout=None)
        origin_lat, origin_lon = self._geocode(geocoder, origin)
        dest_lat, dest_lon = self._geocode(geocoder, dest)

        geojson = self._get_shortest_path_json(hour, origin_lon, origin_lat, dest_lon, dest_lat)

        return JsonResponse(geojson)

    @staticmethod
    def _geocode(geocoder, address):
        """
        Geocode the input address

        Args:
            geocoder (geopy.geocoders.MapBox): MapBox Geocoder
            address (str): address to be geocoded

        Returns:
            latitude (float): latitude of geocoded input address
            longitude (float): longitude of geocoded input address
        """
        location = geocoder.geocode(address)
        return location.latitude, location.longitude

    def _get_shortest_path_json(self, hour, orig_lon, orig_lat, dest_lon, dest_lat):
        """
        Calculate shortest path between origin and destination with weight being crash counts in the specific hour

        Args:
            hour (int): hour
            orig_lon (float): longitude of origin
            orig_lat (float): latitude of origin
            dest_lon (float): longitude of destination
            dest_lat (float): latitude of destination

        Returns:
            geojson (dict): geojson of the corresponding shortest path
        """
        with connection.cursor() as cursor:
            cursor.execute(self._delete_table_query())
            cursor.execute(self._create_table_query(), [hour])
            cursor.execute(self._shortest_path_query(), [orig_lon, orig_lat, dest_lon, dest_lat])
            row = cursor.fetchall()

        geojson = {"type": "FeatureCollection"}

        features = []
        for i in range(len(row)):
            features.append(row[i][0])

        geojson['features'] = features

        return geojson

    @staticmethod
    def _delete_table_query():
        """
        Delete the crash_count table if it already exists

        Returns:
            query (str): a query used to delete the crash_count table if it exists
        """
        return "DROP TABLE IF EXISTS crash_count"

    @staticmethod
    def _create_table_query():
        """
        Create a crash_count table with id, source, target, geometry and costs (crash count) fields

        Returns:
            query (str): a query used to create the crash_count table
        """
        return """
        CREATE TABLE crash_count
        AS (
        WITH cnt AS (
        SELECT network.id,
        network.start as source,
        network.end as target,
        network.geometry,
        count(network.id) as cost
        FROM route_api_drivenetwork AS network
        JOIN route_api_crashes AS crashes
        ON ST_DWithin(network.geometry, crashes.geometry, 0.003)
        WHERE crashes.hour = %s
        GROUP BY network.id
        ) -- crash count of each edge in a particular hour
        SELECT drive.id,
        drive.start::bigint source,
        drive.end::bigint target,
        drive.geometry,
        coalesce(cnt.cost, 0) as cost
        FROM route_api_drivenetwork drive
        LEFT JOIN cnt
        ON drive.id = cnt.id
        ); -- join the drive network table, and fill null with 0
        """

    @staticmethod
    def _shortest_path_query():
        """
        Calculate the shortest path using PostGIS's APIs

        Returns:
            query (str): a query used to calculate the shortest path
        """
        return """
        WITH origin AS (
        SELECT nodes.id,
        nodes.osmid,
        nodes.geometry,
        ST_Distance(nodes.geometry, ST_GeomFromText('POINT(%s %s)', 4326)) AS dist
        FROM route_api_drivenodes nodes
        ORDER BY dist
        LIMIT 1
        ), -- the closest point to the origin
        dest AS (
        SELECT nodes.id,
        nodes.osmid,
        nodes.geometry,
        ST_Distance(nodes.geometry, ST_GeomFromText('POINT(%s %s)', 4326)) AS dist
        FROM route_api_drivenodes nodes
        ORDER BY dist
        LIMIT 1
        ) -- the closest point to the destination
        SELECT json_build_object(
        'type',       'LineString',
        'id',         id,
        'geometry',   ST_AsGeoJSON(geom)::json
        )
        FROM (
        SELECT crash_count.id,
        crash_count.geometry geom
        FROM pgr_dijkstra(
        'SELECT id, source, target, cost FROM crash_count',
        (SELECT osmid::bigint from origin),
        (SELECT osmid::bigint from dest)
        ) AS path -- calculate shortest path
        JOIN crash_count
        ON path.edge = crash_count.id) AS output_table
        """
