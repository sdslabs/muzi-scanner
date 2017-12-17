# Muzi Scanner

This project aims to populate a database with attributes of various songs, given the path to songs root directory.
The songs can be of either mp3 or mp4 or m4a format.

Songs are placed in a hierarchical directory structure inside the songs root directory as follows: 

- Music-Root > Language -> Artist Name > AlbumName > SongName

So, a song "Problem" by Ariana Grande will be in the folder as "Music-Root > English -> Arian Grande > My Everything > Problem.mp3" with rest of "My Everything" album's songs in it. 


## Prerequisites

Install following prerequisites:

- `apt-get install libmysqlclient-dev python-dev python-setuptools`

## Libraries used:

Specified in [requirements.txt]

```sh
$ pip install -r requirements.txt
```

Create a data.json file in the project root. It should look something like below:

```json
{
    "DEFAULT": {
        "lastfm_api_key": "api_key",
        "lastfm_api_secret": "api_secret",
        "db_backend": "mysql",
        "db_name": "test",
        "db_user_name": "test",
        "db_password": "password",
        "db_host": "local"
    },
    "PRODUCTION":{
    }
}
```

## Usage

### Note:

The below command is for development purpose only

```sh
$ python createdb.py
```

Scanner Usage Examples
```sh
$ python scan.py PATH/to/artists/root/ ~/artist_cover_image_directory/ ~/artist_thumbnail_directory/ ~/albums_thumb_image_directory/
```

* Here the PATH/to/artists/root represents the directory where the artists directory are kept and not the music root that is either English or Hindi directory like `/home/fristonio/SDSLabs/music/English` and not `/home/fristonio/SDSLabs/music/`

Example : 

```sh
python scan.py /home/fristonio/SDSLabs/music/English /home/fristonio/SDSLabs/muzi_extras/cdn/band_cover /home/fristonio/SDSLabs/muzi_extras/cdn/band_thumbnail /home/fristonio/SDSLabs/muzi_extras/cdn/album_thumbnail
```

To fix missing thumbnails/coverpics:
```sh
$ python fixmissing.py ~/artist_cover_image_directory/ ~/artist_thumbnail_directory/ ~/albums_thumb_image_directory/
```


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does it's job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [requirements.txt]: <https://raw.githubusercontent.com/GauthamGoli/nefarious-octo-lamp/master/requirements.txt>
   
   

