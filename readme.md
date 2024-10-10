На скриншоте(image.png) прогон через профайлер, так как первая версия долго отрабатывала я решил её переписать на потоки что дало ускорение в ~ 6 раз


<!-- 
первая версия
@profile
def parsing_data_from_profile(target_username: str) -> dict:
    count = 0
    batch_data = []

    followers_by_account = instaloader.Profile.from_username(
        loader.context, target_username
    ).get_followers()

    while count < 50:
        user_data = next(followers_by_account)
        batch_data.append(
            (
                user_data.username,
                user_data.followers,
                user_data.followees,
                user_data.mediacount,
            )
        )

        count += 1
    insert_many_follower_data(batch_data) -->