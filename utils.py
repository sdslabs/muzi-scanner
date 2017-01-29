import urllib
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement
from schema import Track, Album, Band, Year, Genre

class Utils:
    def save_image(self, url, path):
        """
        :param url:
        :param path:
        :return nothing:
        """
        image = urllib.URLopener()
        image.retrieve(url, path)

    def get_or_create(self, session, model, **kwargs):
        try:
            query = session.query(model).filter_by(**kwargs)

            instance = query.first()

            if instance:
                return instance, False
            else:
                try:
                    params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))

                    instance = model(**params)
                    session.add(instance)
                    session.commit()
                    session.refresh(instance)

                    return instance, True
                except IntegrityError as e:
                    # We have failed to add track, rollback current session and continue
                    session.rollback()
                    print "[-]Failed to add, continuing"

        except Exception as e:
            raise e

    def check_if_track_exists(self, variables, file_path):
        session = variables.session()
        query = session.query(Track).filter_by(file=file_path)
        instance = query.first()
        session.close()

        if instance:
            return True
        else:
            return False

    def check_if_band_exists(self, variables, name):
        session = variables.session()
        query = session.query(Band).filter_by(name=name)
        instance = query.first()
        session.close()
        if instance:
            return True, instance.id
        else:
            return False, None

    def check_if_album_exists(self, variables, name, band_name):
        session = variables.session()
        query = session.query(Album).filter_by(name=name, band_name=band_name)
        instance = query.first()
        session.close()
        if instance:
            return True, instance.id
        else:
            return False, None

    def update_model(self, session, model, id, name, info):
        instance = session.query(model).filter_by(id=id).first()
        instance.info = info
        instance.name = name
        session.commit()
        session.close()

    def check_if_album_thumbnail_exists(self, variables):
        return str(variables.album_id) in \
               [img.strip('.jpg') for img in os.listdir(variables.dirs.albums_thumbnail)]

    def check_if_artist_thumbnail_exists(self, variables):
        return str(variables.band_id) in \
               [img.strip('.jpg') for img in os.listdir(variables.dirs.artist_thumbnail)]

    def check_if_artist_cover_exists(self, variables):
        return str(variables.band_id) in \
               [img.strip('.jpg') for img in os.listdir(variables.dirs.artists_cover)]


class Dirs:
    def __init__(self, arguments):
        artists = arguments['artists_dir']
        artists_cover = arguments['artist_cover_dir']
        albums_thumbnail = arguments['album_thumbnail_dir']
        artist_thumbnail = arguments['artist_thumbnail_dir']

        # Convert the path to absolute path
        self.artists = os.path.abspath(artists)

        # Base dir should be where both English and Hindi songs are present
        self.base_dir = os.path.abspath(artists + '/..')

        self.artists_cover = os.path.abspath(artists_cover)
        self.albums_thumbnail = os.path.abspath(albums_thumbnail)
        self.artist_thumbnail = os.path.abspath(artist_thumbnail)


class Variables:
    def __init__(self, arguments, session, network, top_genres):
        self.dirs = Dirs(arguments)
        self.arguments = arguments
        self.session = session
        self.network = network
        self.track_data = {'year':2000,'track_number':'0','track_duration':240,'genre':'unknown'}
        self.tag_data = {'song_title':None,'band_name':None,'album':None,'year':None,'track_duration':None,
                         'track_number':None,'genre':None}
        self.top_genres = top_genres

    def add_band(self, band_name, is_new, band_id = None):
        self.band_id = band_id
        self.is_band_new = is_new
        self.band_name = band_name

    def update_band_status(self, is_new, band_id = None):
        # This method is being made to prevent overwriting of
        # band names
        self.is_band_new = is_new
        self.band_id = band_id

    def add_album(self, album_name, is_new, album_id = None):
        self.album_id = album_id
        self.is_album_new = is_new
        self.album_name = album_name

    def store_track_data(self, keys, values):
        for key,value in zip(keys,values):
            # This case is when value from lastfm is None, we don't want to put that in
            # track_data dictionary
            if (key is "band_name" and self.band_name is not None and value is None) or\
                (key is "album_name" and self.album_name is not None and value is None and\
                         (self.track_data.has_key("album_name") and self.track_data["album_name"] is None)):
                self.track_data[key] = getattr(self, key)
            # This case is when a different album/band song is inside the same album directory
            elif (key is "album_name" and self.album_name != value and value) or\
                    (key is "band_name" and self.band_name != value and value):
                self.track_data[key] = value
                if key is "album_name":
                    instance_exists, instance_id = utils.check_if_album_exists(self,
                                                        name = value,
                                                        band_name = self.tag_data['band_name'])
                    self.is_album_new = not instance_exists
                    if self.is_album_new is False:
                        self.add_album(value, self.is_album_new, instance_id)

                elif key is "band_name":
                    instance_exists, instance_id = utils.check_if_band_exists(self,
                                                        name = value)
                    self.is_band_new = not instance_exists
                    if self.is_band_new is False:
                        # Don't update self.band_name because its the directory's name
                        self.update_band_status(self.is_band_new, instance_id)

            elif (value is None and not self.track_data.has_key(key)) or\
                    (value is not None and self.track_data.has_key(key) and
                             self.track_data[key] != value) or (value is not None):
                self.track_data[key] = value

    def store_tag_data(self, keys, values):
        for key,value in zip(keys,values):
            if (value is not None):
                self.tag_data[key] = value

    def reset_track_data(self):
        self.tag_data = {'song_title':None,'band_name':None,'album':None,'year':None,'track_duration':None,
                         'track_number':None,'genre':None}
        self.track_data = {'year':2000,'track_number':'0','track_duration':240,'genre':'unknown'}

utils = Utils()
