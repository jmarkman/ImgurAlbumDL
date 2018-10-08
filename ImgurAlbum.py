"""Class for interacting with the Imgur API"""
import requests
import os
import errno
import json

class ImgurJSON:
    """Provides interaction with JSON returned from the Imgur API"""
    def __init__(self, url):
        self.web_url = url
        self.json_url = self.__buildJSONUrl()
        self.album_json = None
        self.auth_key = self.__loadClientID()

    def __loadClientID(self):
        self.auth_path = os.path.join(os.path.dirname(__file__), 'auth.json')
        with open(self.auth_path) as authFile:
            authDict = json.loads(authFile.read())     
        return authDict

    def __buildJSONUrl(self):
        slash_location = self.web_url.rindex('/')
        album_id = self.web_url[slash_location + 1:]
        api_url = "https://api.imgur.com/3/album/{0}/images".format(album_id)
        return api_url

    def getAlbumJSON(self):
        """Fetches the JSON for the album from the url provided by the constructor"""
        response = requests.get(self.json_url, headers=self.auth_key)
        self.album_json = response.json()

    def isAccessible(self):
        """Determines if the API query returned successfully"""
        if self.album_json is not None:
            album_status = str(self.album_json["success"])
        if album_status == 'True':
            api_success = True
        else:
            api_success = False
        return api_success

    def downloadImages(self, filepath):
        image_urls = self.__getImageList()
        album_name = self.__getAlbumNameFromURL(self.web_url)
        for url in image_urls:
            # https://imgur.com/a/mo1YAnL
            last_slash = str(url).rindex('/')
            filename = str(url)[last_slash + 1:]
            try:
                os.makedirs(r"{0}\{1}".format(filepath, album_name))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            final_filepath = r"{0}\{1}".format(filepath, album_name)
            with open(r"{0}/{1}".format(final_filepath, filename), "wb") as image:
                image.write(requests.get(url).content)

    def __getAlbumNameFromURL(self, url):
        """Retrieves album name from url"""
        parts = url.split('/')    
        album = parts[len(parts) - 1]
        return album
    
    def __getImageList(self):
        """Retrieves the URLs from the returned JSON"""
        if self.album_json is not None:
            image_data = self.album_json["data"]
        url_list = []
        for image in image_data:
            if image["link"] is not None or image["link"] != "":
                url_list.append(image["link"])
        return url_list



    

    