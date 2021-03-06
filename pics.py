import requests
import pylast
import os
from xml.etree import ElementTree
from utils import utils

class Pics:

    def get_album_thumbnail(self, variables):
        if utils.check_if_album_thumbnail_exists(variables):
            print '[*] ' + variables.album_name + ' thumbnail already exists'
            return
        album_object = variables.network.get_album(variables.band_name, variables.album_name)
        album_id = str(variables.album_id)
        album_image_path = os.path.join(variables.dirs.albums_thumbnail, album_id)+'.jpg'
        try:
            album_cover_image_url = album_object.get_cover_image()
            utils.save_image(album_cover_image_url, album_image_path)
        except Exception as e:
            print "[-] Exception while fetching %s's thumbnail:%s"%(variables.album_name,e.message)
            return
        print '[+] Added ' + variables.album_name + ' thumbnail'

    def get_band_thumbnail(self, variables):
        if utils.check_if_artist_thumbnail_exists(variables):
            print '[*] ' + variables.band_name + ' thumbnail already exists'
            return
        artist_object = variables.network.get_artist(variables.band_name)
        artist_id = str(variables.band_id)
        # Save the artist thumbnails
        artist_thumbnail_path = os.path.join(variables.dirs.artist_thumbnail, artist_id)+'.jpg'
        # Note the size argument which returns the url for a smaller image
        try:
            utils.save_image(artist_object.get_cover_image(size=2), artist_thumbnail_path)
        except Exception as e:
            print "[-] Exception while fetching %s's thumbnail: %s"%(variables.band_name,e.message)
            return
        print '[+] Added ' + variables.band_name + ' thumbnail'

    def get_band_cover(self, variables):
        if utils.check_if_artist_cover_exists(variables):
            print '[*] ' + variables.band_name + ' cover images already exists'
            return
        zune_root = 'http://catalog.zune.net/v3.2/en-US/music/artist'
        response = requests.get(zune_root, params = { 'q': variables.band_name })
        artist_cover_path = os.path.join(variables.dirs.artists_cover,
                                         str(variables.band_id)) + '.jpg'

        if response.status_code == 200:
            xml_tree = ElementTree.fromstring(response.content)
            # Namespace for XML
            ns = { 'a': 'http://www.w3.org/2005/Atom',
                   'zune': 'http://schemas.zune.net/catalog/music/2007/10' }
            try:
                uuid = xml_tree.find('a:entry', ns).find('a:id', ns).text[9:]
            except Exception as e:
                self.get_band_cover_from_lastfm(variables)
                return

            response = requests.get(zune_root + '/' + uuid + '/images')
            xml_tree = ElementTree.fromstring(response.content)
            entries = xml_tree.findall('a:entry', ns)
            width = 0
            url = None
            # Get widest length cover pic
            for e in entries:
                instance = e.find('zune:instances', ns).find('zune:imageInstance', ns)
                url = instance.find('zune:url', ns).text
                break
            if not url:
                self.get_band_cover_from_lastfm(variables)
                return
            utils.save_image(url, artist_cover_path)
            print '[+] Added ' + variables.band_name + ' cover'

    def get_band_cover_from_lastfm(self, variables):
        print ' [+] Cover pic not found in Zune, trying to fetch from lastfm'
        artist_object = variables.network.get_artist(variables.band_name)
        artist_id = str(variables.band_id)
        # Save the artist thumbnails
        artist_cover_path = os.path.join(variables.dirs.artists_cover, artist_id)+'.jpg'
        # Note the size argument which returns the url for a smaller image
        try:
            utils.save_image(artist_object.get_cover_image(), artist_cover_path)
        except Exception as e:
            print "[-] Exception while fetching %s's cover pic: %s"%(variables.band_name,e.message)
            return
        print "[+] Added %s's cover"%(variables.band_name)

pics = Pics()
