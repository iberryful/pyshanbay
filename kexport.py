import sqlite3

def export_kindle_words(db_path = 'vocab.db', output = 'kwords.txt'):
    conn = sqlite3.connect(db_path)
    with open(output, 'w') as f:
        for row in conn.execute('SELECT * FROM WORDS'):
            if 'en:' in row[0]:
                f.write(row[2] + "\n")
    conn.close()

if __name__ == '__main__':
    export_kindle_words()
