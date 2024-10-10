import concurrent.futures
import instaloader
import os
from dotenv import load_dotenv
from line_profiler import profile
from database import create_database, insert_many_follower_data

load_dotenv()

loader = instaloader.Instaloader(
    max_connection_attempts=1,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
)

username = os.getenv("USER")
password = os.getenv("PASSWORD")

loader.load_session_from_file(username)


def fetch_follower_data(follower: dict):
    return (
        follower.username,
        follower.followers,
        follower.followees,
        follower.mediacount,
    )


@profile
def parsing_data_from_profile(target_username: str):
    follower_node = instaloader.Profile.from_username(
        loader.context, target_username
    ).get_followers()

    batch_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(fetch_follower_data, next(follower_node)) for _ in range(50)
        }

        for future in concurrent.futures.as_completed(futures):
            batch_data.append(future.result())
        insert_many_follower_data(batch_data)


create_database()
parsing_data_from_profile(target_username="skillbox.ru")
