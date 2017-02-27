import requests
import json
import time

BASE_URL = "https://api.shanbay.com"
METHOD_MAP = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put
}


class API():
    def __init__(self, config_path="config.json"):
        self.config = self.load_config()
        print("load config success.")
        if "expires_at" not in self.config or self.config['expires_at'] < time.time():
            print("auth info is not valid, please auth.")
            self.auth()
        else:
            print("auth info found")

    def load_config(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            return json.loads(f.read())

    def save_config(self, config_path="config.json"):
        with open(config_path, 'w') as f:
            return f.write(json.dumps(self.config, indent=4))

    def _make_url(self, path, *args, **kwargs):
        return BASE_URL + path + "?" + "&".join(["%s=%s" % (arg, self.config[arg]) for arg in args])

    def auth(self):
        print("please open the following link in browser and input return code.")
        print(self._make_url("/oauth2/authorize/", "client_id", "response_type"))
        code = input("Input code:")
        self.config['code'] = code
        r = requests.post(self._make_url("/oauth2/token/", "client_id", "client_secret", "code",
                                         "redirect_uri", "grant_type"))
        if not r.status_code == 200:
            print("Erros in auth process.")
            exit(1)
        self.config.update(r.json())
        self.config['expires_at'] = int(time.time()) + self.config['expires_in']
        self.save_config()

    def __getattr__(self, attr):
        if attr in METHOD_MAP:
            def wrapper(path, *args, **kw):
                headers = {
                    "Authorization": self.config['token_type'] + ' ' + self.config['access_token']
                }
                url = BASE_URL + path
                return METHOD_MAP[attr](url, *args, **kw, headers=headers)

            return wrapper


if __name__ == '__main__':
    api = API()
    r = api.get('/bdc/search/', {"word": "anneal"})
    print(r.content)

