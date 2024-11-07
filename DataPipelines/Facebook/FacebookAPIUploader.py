from ..Base.Uploader import Uploader
import requests
from urllib.parse import urlparse

class FacebookGroupUploader(Uploader):
    def __init__(self, formatted_data, access_token, group_id, image_source):
        super().__init__(formatted_data)
        self.access_token = access_token
        self.group_id = group_id
        self.image_source = image_source

    def _upload_image(self):
        url = f"https://graph.facebook.com/v12.0/{self.group_id}/photos"
        
        params = {
            'access_token': self.access_token,
            'published': 'false'
        }

        if self._is_url(self.image_source):
            # If image_source is a URL, pass it directly to Facebook
            params['url'] = self.image_source
            response = requests.post(url, params=params)
        else:
            # If image_source is a local path, open and send the file
            with open(self.image_source, 'rb') as image_file:
                files = {'source': image_file}
                response = requests.post(url, params=params, files=files)
        
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise Exception(f"Failed to upload image: {response.text}")

    def _is_url(self, string):
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    # ... rest of the class remains the same ...

# Example usage:
# Local file:
# uploader = FacebookGroupUploader("Check out this local image!", "ACCESS_TOKEN", "GROUP_ID", "/path/to/local/image.jpg")

# URL:
# uploader = FacebookGroupUploader("Check out this online image!", "ACCESS_TOKEN", "GROUP_ID", "https://example.com/image.jpg")