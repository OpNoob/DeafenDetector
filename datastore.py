import pickle
import os


class GuildData:
    def __init__(self, guild_id: int = None):
        self._guild_id = guild_id
        self.deafen_targets = set()

    def toDict(self):
        return self.__dict__

    @property
    def guild_id(self):
        return self._guild_id

    def addDeafenTarget(self, user_id):
        self.deafen_targets.add(user_id)

    def removeDeafenTarget(self, user_id):
        self.deafen_targets.remove(user_id)


class DeafenData:
    def __init__(self):
        self.count = 0
        self.time_taken = 0

    def add(self, count=0, time=0):
        self.count += count
        self.time_taken += time


class UserData:
    def __init__(self, user_id: int = None):
        self._user_id = user_id
        self.deafen_data = DeafenData()

    @property
    def user_id(self):
        return self._user_id


class Database:
    def __init__(self, path='data/database.pkl'):
        self._path = path

        self.root = dict()
        self._loaded = self.load()

        self.guild_data = self.getTable("guild_data")
        self.user_data = self.getTable("user_data")

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "rb") as f:
                self.root = pickle.load(f)
                return True
        else:
            return False

    def commit(self):
        with open(self._path, "wb") as f:
            pickle.dump(self.root, f)

    def getTable(self, table_name):
        if table_name not in self.root:
            self.root[table_name] = dict()
        data = self.root[table_name]
        return data

    # Guild Data: Deafen
    def addDeafenTrack(self, guild_id: int, user_id: int):
        if guild_id in self.guild_data:
            guild_data = self.guild_data[guild_id]
        else:
            guild_data = GuildData(guild_id)
            self.guild_data[guild_id] = guild_data
        guild_data.addDeafenTarget(user_id)

    # Guild Data: Deafen
    def removeDeafenTrack(self, guild_id: int, user_id: int):
        if guild_id in self.guild_data:
            guild_data = self.guild_data[guild_id]
            guild_data.deafen_targets.remove(user_id)

    # Guild Data: Deafen
    def getDeafenTracks(self):
        """
        :return: {user_id: {guild_ids}}
        """
        dict_map = dict()
        for guild_id, item in self.guild_data.items():
            for user_id in item.deafen_targets:
                if user_id in dict_map:
                    dict_map[user_id].add(guild_id)
                else:
                    dict_map[user_id] = {guild_id}
        return dict_map

    # User Data: Deafen
    def addDeafenData(self, user_id: int, count=1, time=0):
        if user_id in self.user_data:
            user_data = self.user_data[user_id]
        else:
            user_data = UserData(user_id)
            self.user_data[user_id] = user_data
        user_data.deafen_data.add(count=count, time=time)

    # User Data: Deafen
    def getDeafenData(self, user_id: int):
        if user_id in self.user_data:
            user_data = self.user_data[user_id]
            return user_data.deafen_data


if __name__ == "__main__":
    dd = Database()
    # print(dd.getDeafenTracks())
    # dd.addDeafenTrack(123123123123, 234)
    # dd.addDeafenTrack(123123123123, 2344)
    #
    # dd.commit()
    print(dd.getDeafenTracks())
