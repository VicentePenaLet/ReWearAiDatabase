import instaloader
import time
import pandas as pd

def login(user = "victoriagomez9021", password = "98vp98"):
    L = instaloader.Instaloader()
    L.login(user, password)
    return L

class LocalDatabase():
    def __init__(self, ig_session = None, load_local = True, profile_file = 'Profiles.txt', database_profiles = "Database_profiles.csv",
                 database_posts = "Database_post.csv"):
        super().__init__()
        if ig_session:
            self.ig_session = ig_session
        if load_local:
            try:
                self.profiles_table = pd.read_csv(database_profiles)
                self.post_table = pd.read_csv(database_posts)
            except:
                self.create_user_database(profile_file)
                self.download_users_post()
        else:
            self.create_user_database(profile_file)
            self.download_users_post()

    def create_user_database(self, file):
        print("Creating Database")
        profiles_file = open(file, 'r')
        profiles_usernames = profiles_file.readlines()

        profiles_table = {}
        usernames = []
        user_ids = []
        for username in profiles_usernames:
            username = username.strip()
            profile = instaloader.Profile.from_username(self.ig_session.context, username)
            usernames.append(username)
            user_ids.append(profile.userid)
        profiles_table = {"Username": usernames,
                          "User id": user_ids}
        self.profiles_table = pd.DataFrame(profiles_table)
        self.profiles_table.to_csv("Database_profiles.csv")

    def download_users_post(self):
        post_shortcode = []
        post_title = []
        post_owner_username = []
        post_owner_id = []
        post_date_utc = []
        post_url = []
        post_typename = []
        post_caption = []
        # post_path = []
        print("Creating Post Database")
        for index, row in self.profiles_table.iterrows():
            print(row["Username"])
            profile = instaloader.Profile.from_username(self.ig_session.context, row["Username"])
            n = 0
            for post in profile.get_posts():
                print(post)
                time.sleep(10)
                post_shortcode.append(post.shortcode)
                post_title.append(post.title)
                post_owner_username.append(post.owner_username)
                post_owner_id.append(post.owner_id)
                post_date_utc.append(post.date_utc)
                post_url.append(post.url)
                post_typename.append(post.caption)
                post_caption.append(post.pcaption)
                # post_path.append("{}/".format(row["Username"]))
                self.ig_session.download_post(post, target=profile.username)
                n += 1
                if n > 5:
                    break
        post_table = {"Owner": post_owner_username,
                      "Shortcode": post_shortcode,
                      "Date": post_date_utc,
                      "Typename": post_typename}


        self.post_table = pd.DataFrame(post_table)
        self.post_table.to_csv("Database_post.csv")


if __name__ == "__main__":
    l = login()
    db = LocalDatabase(l, load_local=False)

    #for post in profile.get_posts():
    #    time.sleep(10)
    #    print(post)
    #    L.download_post(post, target=profile.username)


