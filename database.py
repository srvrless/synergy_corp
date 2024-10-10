import sqlite3


def create_database():
    conn = sqlite3.connect("followers_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        username TEXT PRIMARY KEY,
        followers_count INTEGER,
        followees_count INTEGER,
        posts_count INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_many_follower_data(followers_data: list):
    conn = sqlite3.connect("followers_data.db")
    cursor = conn.cursor()
    conn.execute("BEGIN TRANSACTION")
    cursor.executemany(
        """
    INSERT OR REPLACE INTO followers (username, followers_count, followees_count, posts_count)
    VALUES (?, ?, ?, ?)
    """,
        followers_data,
    )

    conn.commit()

    conn.close()
