import sqlite3

conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()
def main():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL UNIQUE,
            text1 TEXT,
            text2 TEXT,
            text3 TEXT,
            text4 TEXT,
            confirm INT,
            photo2 TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            user_id INT NOT NULL UNIQUE,
            card TEXT,
            fio TEXT
        );
    ''')

#Заявки
def add_user(user_id: int):
    cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
def add_text1(text1: str, user_id1, file_id):
    cursor.execute(f'INSERT OR REPLACE INTO users (user_id, text1, text2, text3, text4, confirm, photo2) VALUES (?,?,?,?,?,?,?)', (user_id1, text1, None, None, None, 0, file_id))
    conn.commit()
def add_text2(text1: str, text2: str, user_id1, file_id):
    cursor.execute(f'INSERT OR REPLACE INTO users (user_id, text1, text2, text3, text4, confirm, photo2) VALUES (?,?,?,?,?,?,?)', (user_id1, text1, text2, None, None, 0, file_id))
    conn.commit()
def add_text3(text1: str, text2:str, text3: str, user_id1, file_id):
    cursor.execute(f'INSERT OR REPLACE INTO users (user_id, text1, text2, text3, text4, confirm, photo2) VALUES (?,?,?,?,?,?,?)', (user_id1, text1, text2, text3, None, 0, file_id))
    conn.commit()
def add_text4(text1: str, text2:str, text3: str, text4: str, user_id1, file_id):
    cursor.execute(f'INSERT OR REPLACE INTO users (user_id, text1, text2, text3, text4, confirm, photo2) VALUES (?,?,?,?,?,?,?)', (user_id1, text1, text2, text3, text4, 0, file_id))
    conn.commit()
def add_confirm(text1: str, text2:str, text3: str, text4: str, user_id1, confirm: int, file_id):
    cursor.execute(f'UPDATE users SET confirm={confirm} WHERE user_id = {user_id1}')
    conn.commit()

#Работа с картами 
def get_card():
    cursor.execute(f'SELECT card FROM data')
    jon = cursor.fetchone()
    return jon[0] if jon else None

def get_fio():
    cursor.execute(f'SELECT fio FROM data')
    jon = cursor.fetchone()
    return jon[0] if jon else None

def add_card(user_id, card):
    cursor.execute('INSERT OR REPLACE INTO data (user_id, card) VALUES (?, ?)', (user_id, card))
    conn.commit()


def add_fio(user_id, fio, card):
    cursor.execute('INSERT OR REPLACE INTO data (user_id, fio, card) VALUES (?, ?, ?)', (user_id, fio, card))
    conn.commit()



def get_conf(user_id1):
    cursor.execute(f'SELECT confirm FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchone()
    return jon[0]
    
def get_text1(user_id1):
    cursor.execute(f'SELECT text1 FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchone()
    return jon[0]
def get_text2(user_id1):
    cursor.execute(f'SELECT text2 FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchone()
    return jon[0]
def get_text3(user_id1):
    cursor.execute(f'SELECT text3 FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchone()
    return jon[0]
def get_zaya(user_id1):
    cursor.execute(f'SELECT * FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchall()
    return jon[0][3]
def get_photo(user_id1):
    cursor.execute(f'SELECT photo2 FROM users WHERE user_id={user_id1}')
    jon = cursor.fetchone()
    return jon[0]
def get_confirm_status(user_id1):
    cursor.execute(f'SELECT confirm FROM users WHERE user_id={user_id1}')
    result = cursor.fetchone()
    if result:
        return result[0]
    return None
def get_all_users():
        cursor.execute('SELECT user_id FROM users ')
        users = [row[0] for row in cursor.fetchall()]
        return users


if __name__ == '__main__':
    main()
