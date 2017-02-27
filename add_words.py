import click
from pyshanbay import API


class WordsAdder(API):
    def __init__(self, *args, **kwargs):
        API.__init__(self, *args, **kwargs)

    def load_words(self, path="kwords.txt"):
        with open(path, 'r') as f:
            return f.read().split('\n')

    def add_a_word(self, word):
        r = self.get('/bdc/search/', {'word': word})
        if r.status_code != 200:
            print('request error\n')
            exit(1)
        r = r.json()
        if r['status_code'] != 0:
            print(r['msg'])
            return
        if "learning_id" in r['data']:
            print(word + " is in learning, skip")
            return
        r = self.post('/bdc/learning/', {"id": r['data']['id']})
        print(word, r.json()['msg'])

    def add_words(self, words):
        list(map(self.add_a_word, words))


@click.command()
@click.option("-c", "--config", default="config.json", help="path to config file")
@click.option("-i", "--inputs", default="kwords.txt", help="path to words file")
def main(config, inputs):
    wa = WordsAdder(config)
    wa.add_words(wa.load_words(inputs))


if __name__ == '__main__':
    main()
