class SpotifyService:
    def __init__(self, access_code):
        self._access_code = access_code

    def test_connection(self):
        print(f'Accessing Spotify with {self._access_code}')


class SpotifyServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, spotify_client_key, spotify_client_secret, **_ignored):
        if not self._instance:
            access_code = self.authorize(
                spotify_client_key, spotify_client_secret)
            self._instance = SpotifyService(access_code)
        return self._instance

    def authorize(self, key, secret):
        return 'SPOTIFY_ACCESS_CODE'


class PandoraService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')


class PandoraServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, pandora_client_key, pandora_client_secret, **_ignored):
        if not self._instance:
            consumer_key, consumer_secret = self.authorize(
                pandora_client_key, pandora_client_secret)
            self._instance = PandoraService(consumer_key, consumer_secret)
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'


class LocalService:
    def __init__(self, location):
        self._location = location

    def test_connection(self):
        print(f'Accessing Local music at {self._location}')


def create_local_music_service(local_music_location, **_ignored):
    return LocalService(local_music_location)


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


if __name__ == '__main__':
    config = {
        'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
        'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
        'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
        'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
        'local_music_location': '/usr/data/music'
    }

    factory = ObjectFactory()
    factory.register_builder('SPOTIFY', SpotifyServiceBuilder())
    factory.register_builder('PANDORA', PandoraServiceBuilder())
    factory.register_builder('LOCAL', create_local_music_service)

    pandora = factory.create('PANDORA', **config)
    pandora.test_connection()
    spotify = factory.create('SPOTIFY', **config)
    spotify.test_connection()
    local = factory.create('LOCAL', **config)
    local.test_connection()
    pandora2 = music.services.get('PANDORA', **config)
    print(f'id(pandora) == id(pandora2): {id(pandora) == id(pandora2)}')
    spotify2 = music.services.get('SPOTIFY', **config)
    print(f'id(spotify) == id(spotify2): {id(spotify) == id(spotify2)}')

