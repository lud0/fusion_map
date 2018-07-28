import httplib2
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class FusionTable:

    def __init__(self, credentials, table_id):
        scopes = ['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scopes=scopes)
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.service = build('fusiontables', 'v2', http=http)
        self.table_id = table_id

    def location_exists(self, lat, lon):
        sql = "SELECT * FROM {table_id} WHERE Location='{latlon}'"
        sql = sql.format(table_id=self.table_id, latlon=','.join([lat, lon]))
        result = self.service.query().sqlGet(sql=sql).execute()
        return 'rows' in result

    def add_location(self, address, lat, lon):
        sql = "INSERT INTO {table_id} (Text, Location) VALUES ('{address}', '{latlon}')"
        address = address.replace("'", "\\'")
        sql = sql.format(table_id=self.table_id, address=address, latlon=','.join([lat, lon]))
        self.service.query().sql(sql=sql).execute()

    def remove_all(self):
        sql = "DELETE FROM {table_id}".format(table_id=self.table_id)
        self.service.query().sql(sql=sql).execute()
