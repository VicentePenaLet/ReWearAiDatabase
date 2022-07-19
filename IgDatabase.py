import instaloader
import time
import pandas as pd
import glob, os
import csv
import shutil

class LocalDatabase():
    def __init__(self, root = ".", create = False, database_file = "Post_Database.csv"):
        super().__init__()
        self.root = root
        if create:
            self.create_database()
        else:
            self.Database = pd.read_csv(database_file)

    def create_database(self):
        os.chdir(self.root+"/DB")
        tables = []
        for file in glob.glob("*.csv"):
            df = pd.read_csv(file)
            username = df.iloc[0][0]
            df = df.drop(0)
            print(df.columns)
            df.columns = ['Path', 'Caption', 'Link']
            df["Username"] = username
            tables.append(df)
            path = username
            if not os.path.exists(path):
                os.makedirs(path)
                print("The new directory {} is created!".format(path))
            new_paths = []
            for image in df["Path"]:
                head, tail = os.path.split(image)
                new_path = os.path.join(path, tail)
                if image.split(".")[-1] == "jpg":
                    shutil.copyfile(image, new_path)
                new_paths.append(new_path)
            df["Path"] = new_paths
        self.Database = pd.DataFrame(columns= ['Path', 'Caption', 'Link', 'Username'])
        for table in tables:
            self.Database = self.Database.append(table, ignore_index=True)
        self.Database.to_csv("../Post_Database.csv")


class LocalDatabase1():
    def __init__(self, ig_session = None, load_local = True, database_profiles = "Database_profiles.csv",
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
            profile = instaloader.Profile.from_id(self.ig_session.context, username)
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
            print(row["User id"])
            profile = instaloader.Profile.from_id(self.ig_session.context, row["User id"])
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
                self.ig_session.download_pic(f"/{profile.username}/{post_shortcode}", post_url, post_url)
                n += 1
                if n > 50:
                    break

        post_table = {"Owner": post_owner_username,
                      "Shortcode": post_shortcode,
                      "Date": post_date_utc,
                      "Typename": post_typename}


        self.post_table = pd.DataFrame(post_table)
        self.post_table.to_csv("Database_post.csv")


if __name__ == "__main__":
    db = LocalDatabase(database_file= "Post_Database.csv")
    print(db.Database.iloc[0])
    #for post in profile.get_posts():
    #    time.sleep(10)
    #    print(post)
    #    L.download_post(post, target=profile.username)


