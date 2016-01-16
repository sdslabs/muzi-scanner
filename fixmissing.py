__author__ = 'gautham'

import os
import sys
import pylast
import credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schema import Album, Band
from utils import utils, Variables
from pics import pics

class ImageFixer:

    def download_missing_images(self, variables):
        artists_cover = variables.dirs.artists_cover
        artist_thumbnail = variables.dirs.artist_thumbnail
        albums_thumbnail = variables.dirs.albums_thumbnail

        downloader = [pics.get_band_cover, pics.get_band_thumbnail, pics.get_album_thumbnail]

        iterable_list = [(Band, artists_cover), (Band, artist_thumbnail), (Album, albums_thumbnail)]

        for index, (model, directory) in enumerate(iterable_list):
            # Find all model ids which are already downloaded
            model_ids_with_image = [img.strip('.jpg') for img in os.listdir(directory)]
            # Find the contra model set for the above list
            models_without_image = variables.session().query(model).filter\
                                             (~model.id.in_(model_ids_with_image)).all()

            for model in models_without_image:
                if model.__class__ is Band:
                    variables.add_band(model.name, False, model.id)
                    variables.add_album(None, False, None)
                elif model.__class__ is Album:
                    # Both album, band variables are required to download album related images
                    variables.add_band(model.band_name, False, model.band_id)
                    variables.add_album(model.name, False, model.id)
                downloader[index](variables)

    def __init__(self, arguments):

        # Configure Session class with desired options
        Session = sessionmaker()

        # Import credentials
        db_name = credentials.get_db_name()
        db_user_name = credentials.get_db_user_name()
        db_host = credentials.get_db_host()
        db_password = credentials.get_db_password()
        db_backend = credentials.get_db_backend()

        # Later, we create the engine
        engine = create_engine('{backend}://{user}:{password}@{host}/{name}?charset=utf8'
                                .format(backend=db_backend,
                                        user=db_user_name,
                                        password=db_password,
                                        host=db_host,
                                        name=db_name),
                                        # echo=True
                                        )

        # Associate it with our custom Session class
        Session.configure(bind=engine)

        # API Credentials
        API_KEY = credentials.get_lastfm_api_key()
        API_SECRET = credentials.get_lastfm_api_secret()
        DB_NAME = credentials.get_db_name()

        network = pylast.LastFMNetwork(api_key=API_KEY,
                                       api_secret=API_SECRET,)

        variables = Variables(arguments, Session, network)

        self.download_missing_images(variables)

if __name__ == '__main__':

    arguments = {'artists_dir':'', 'artist_cover_dir': sys.argv[1],
                 'artist_thumbnail_dir': sys.argv[2], 'album_thumbnail_dir': sys.argv[3]}

    ImageFixer(arguments)