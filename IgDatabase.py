import instaloader
import time
import pandas as pd

def login():
    L = instaloader.Instaloader()
    L.login("vicenteeduardoiii", "g.e.1234")
    return L

class LocalDatabase():
    def __init__(self, ig_session, load_local = True, profile_file = 'Profiles.txt'):
        super().__init__()
        self.ig_session = ig_session
        if load_local:
            try:
                self.profiles_table = pd.read_csv("profiles_table.csv")
            except:
                self.create_user_database(profile_file)
        else:
            self.create_user_database(profile_file)
        print("Profiles Loaded")
        post_shortcode = []
        post_title = []
        post_owner_username = []
        post_owner_id = []
        post_date_utc = []
        post_url = []
        post_typename = []
        post_caption = []
        #post_path = []
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
                #post_path.append("{}/".format(row["Username"]))
                self.ig_session.download_post(post, target=profile.username)
                n+=1
                if n > 5:
                    break
        self.post_table = {"Owner": post_owner_username,
                      "Caption:": post_caption,
                      "Shortcode": post_shortcode,
                      "Title": post_title,
                      "Date": post_date_utc,
                      "Typename": post_typename}
        self.post_table = pd.DataFrame(post_table)
        self.post_table.to_hdf("Post_Table.hdf")



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
        self.profiles_table.to_hdf("profiles_table.hdf")

    def download_users_post(self):
        pass


if __name__ == "__main__":
    L = login()
    db = LocalDatabase(L)

    #for post in profile.get_posts():
    #    time.sleep(10)
    #    print(post)
    #    L.download_post(post, target=profile.username)

