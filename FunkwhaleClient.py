import requests
from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from pprint import pprint
from mutagen.easyid3 import EasyID3


class FunkwhaleClient:

    def __init__(self, url, token):
        self._url = url + 'api/v1' if url[-1] == '/' else url + '/api/v1'
        self._token = token
        self._headers = {'Authorization': 'Bearer {}'.format(self._token)}

        try:
            url = self._url + '/playlists/'
            response = requests.get(url, headers=self._headers)
            assert response.status_code == 200
            assert isinstance(response.json()["results"], list)
        except:
            raise Exception("Cannot connect to Funkwhale server with url: {} and token: {}".format(self._url, self._token))

    def except_msg(self, response, http_code):
        try:
            assert response.status_code == http_code
        except:
            raise Exception("Funkwhale api error : " + response.text)

    def list_playlists(self):
        url = self._url + '/playlists/'
        response = requests.get(url, headers=self._headers)
        self.except_msg(response, 200)
        return response.json()['results']

    def _create_callback(self, encoder):
        encoder_len = encoder.len
        bar = ProgressBar(expected_size=encoder_len, filled_char='=')
        def callback(monitor):
            bar.show(monitor.bytes_read)
        return callback

    def create_playlist(self, name, privacy_level):
        url = self._url + '/playlists/'
        name = name if len(name) < 50 else name[0:50] # cut playlist name at 50 chars
        data = { 'name' : name, 'privacy_level': privacy_level }
        response = requests.post(url, headers=self._headers, json=data)
        self.except_msg(response, 201)
        playlist_id = response.json()["id"]
        return playlist_id

    def add_to_playlist(self, track_id, playlist_id):
        url = self._url + '/playlists/' + str(playlist_id) + '/add'
        data = { 'tracks' : [track_id], 'allow_duplicates': False }
        response = requests.post(url, headers=self._headers, json=data)
        if response.status_code == 201:
            results = response.json()["results"]
            return results
        else:
            assert "tracks_already_exist_in_playlist" in response.text
            return None

    def delete_playlist(self, playlist_id):
        url = self._url + '/playlists/' + str(playlist_id)
        response = requests.delete(url, headers=self._headers)
        self.except_msg(response, 204)
        return playlist_id

    def create_upload(self, filename, library_id):
        url = self._url + '/uploads/'
        with open(filename, 'rb') as audio_file:
            encoder = MultipartEncoder({
                'audio_file': (filename, audio_file, 'audio/mpeg'),
                'library': library_id,
                'import_reference': 'funkdl',
                'import_status': 'pending'
            })
            callback = self._create_callback(encoder)
            monitor = MultipartEncoderMonitor(encoder, callback)
            headers = self._headers | {'Content-Type': monitor.content_type}
            print(filename + '   ')
            response = requests.post(url, headers=headers, data=monitor)
        self.except_msg(response, 201)
        upload_uuid = response.json()["uuid"]
        return upload_uuid

    def get_track_id_from_upload(self, upload_uuid):
        url = self._url + '/uploads/' + str(upload_uuid)
        response = requests.get(url, headers=self._headers)
        self.except_msg(response, 200)
        return response.json()["track"]["id"]

    def get_track_id_from_metadata(self, file_path):
        audio_file_metadata = EasyID3(file_path)
        search_string = audio_file_metadata['title'][0] + ' ' + audio_file_metadata['artist'][0]
        url = self._url + '/uploads/'
        params = { 'q': search_string }
        response = requests.get(url, headers=self._headers, params=params)
        self.except_msg(response, 200)
        return response.json()['results'][0]["track"]["id"]

    def activate_upload(self, upload_uuid):
        url = self._url + '/uploads/' + str(upload_uuid)
        data = { 'import_status': 'pending'}
        response = requests.patch(url, headers=self._headers, data=data)
        self.except_msg(response, 200)
        print('prout')
        pprint(response.json())
        return response.json()

