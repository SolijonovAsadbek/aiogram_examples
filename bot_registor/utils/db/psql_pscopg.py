import psycopg2

from data.config import DB_NAME, USER, PASSWORD, HOST, PORT

db_url = f"dbname={DB_NAME} user={USER} password={PASSWORD} host={HOST} port={PORT}"
conn = psycopg2.connect(db_url)
curr = conn.cursor()


def followers():
    query = "SELECT COUNT(*) FROM users;"
    curr.execute(query)
    count = curr.fetchone()
    return count


def get_by_id(id_):
    query = f"SELECT * FROM users WHERE chat_id={id_};"
    curr.execute(query)
    user = curr.fetchone()
    return user


def save_user(chat_id, username, fullname, phone, address, birthday):
    query = f"""INSERT INTO users (chat_id, username, fullname, phone, address, birthday) 
    VALUES ({chat_id}, '{username}','{fullname}', '{phone}', '{address}', '{birthday}' );"""
    with conn:
        curr.execute(query)
