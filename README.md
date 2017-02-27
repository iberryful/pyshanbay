# pyshanbay
Pyshanbay provides fundament tools to access shanbay(shanbay.com), including Oauth2 and a simple wrapper to build your own application.

## API usage
* Add config file, config.json

```json
{
    "redirect_uri": "http://example.com/callback?....",
    "client_id": "xxxxxxxxx",
    "grant_type": "authorization_code"
}
```
* Auth

```python
api = API(config_path) #default: config.json
```
Access auth url in the browser and paste code in redirection url to the prompt.

Auth is needed when first use or token is expired.

* API tool

You can build your own api by using `api.get()   api.post()` and so on.

```
r = api.get('/bdc/search/', {"word": "anneal"}) #search word
r = api.post('/bdc/learning/',{"id": 14700}) #add word
```

## Kindle export tool
You can export your kindle vocabulary db to a txt file, which is stored in `[kindle]/system/vocabulary/vocab.db`

```shell
$ python kexport.py -i vocab.db -o kwords.txt
```

## Add words to shanbay
You can add plenty of words to your shanbay account by `add_words.py`


```shell
$ python add_words.py -c config.json -i kwords.txt
```

 



