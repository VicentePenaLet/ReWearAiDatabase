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

if __name__ == "__main__":
    db = LocalDatabase(database_file= "Post_Database.csv")
    print(db.Database.iloc[0])



