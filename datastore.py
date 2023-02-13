import sqlite3


class Datastore:
    def __init__(self, path="data/database.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()

        sql = "CREATE TABLE IF NOT EXISTS guild_data (" \
              "ID int NOT NULL PRIMARY KEY" \
              ");"
        self.cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS user_data (" \
              "ID int NOT NULL PRIMARY KEY, " \
              "deafen_count int DEFAULT 0" \
              ");"
        self.cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS guild_users (" \
              "ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "guild_id int, " \
              "user_id int, " \
              "track_deafen BIT default 'FALSE', " \
              "FOREIGN KEY (guild_id) REFERENCES guild_data(ID), " \
              "FOREIGN KEY (user_id) REFERENCES user_data(ID), " \
              "UNIQUE(guild_id, user_id)" \
              ");"
        self.cur.execute(sql)

        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def addGuild(self, guild_id: int):
        sql = "INSERT INTO guild_data (ID) " \
              "SELECT ?1 WHERE NOT EXISTS(SELECT * FROM guild_data WHERE ID=?1)"
        self.cur.execute(sql, (guild_id,))
        self.commit()

    def getGuildIDS(self):
        sql = "SELECT ID FROM guild_data"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return [r[0] for r in result]

    def addUser(self, user_id: int):
        sql = "INSERT INTO user_data (ID) " \
              "SELECT ?1 WHERE NOT EXISTS(SELECT * FROM user_data WHERE ID=?1)"
        self.cur.execute(sql, (user_id,))
        self.commit()

    def getUserIDS(self):
        sql = "SELECT ID FROM user_data"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return [r[0] for r in result]

    def addDeafenTrack(self, guild_id: int, user_id: int):
        # Ensuring no errors
        self.addGuild(guild_id)
        self.addUser(user_id)

        insert_sql = "INSERT OR IGNORE INTO guild_users (guild_id, user_id, track_deafen) " \
                     "VALUES(?1, ?2, 'TRUE')"
        update_sql = "UPDATE guild_users SET track_deafen='TRUE' WHERE guild_id=?1 AND user_id=?2"

        self.cur.execute(insert_sql, (guild_id, user_id))
        self.cur.execute(update_sql, (guild_id, user_id))
        self.commit()

    def removeDeafenTrack(self, guild_id: int, user_id: int):
        sql = "UPDATE guild_users " \
              "SET track_deafen = 'FALSE' " \
              "WHERE guild_id=? AND user_id=?;"
        self.cur.execute(sql, (guild_id, user_id))
        self.commit()

    def getDeafenTracks(self):
        """
        :return: {user_id: {guild_ids}}
        """

        sql = "SELECT guild_id, user_id FROM guild_users;"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        dict_map = dict()
        for guild_id, user_id in result:
            if user_id in dict_map:
                dict_map[user_id].add(guild_id)
            else:
                dict_map[user_id] = {guild_id}

        return dict_map

    def getDeafenTracksINV(self):
        """
        :return: {guild_id: {user_ids}}
        """

        sql = "SELECT guild_id, user_id FROM guild_users;"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        dict_map = dict()
        for guild_id, user_id in result:
            if guild_id in dict_map:
                dict_map[guild_id].add(user_id)
            else:
                dict_map[guild_id] = {user_id}

        return dict_map

    def addDeafenData(self, user_id: int, count=1):
        # User exists is assumed here
        sql = "UPDATE user_data " \
              "SET deafen_count = deafen_count + ? " \
              "WHERE ID = ?"
        self.cur.execute(sql, (count, user_id))

    def getDeafenData(self, user_id: int):
        sql = "SELECT deafen_count FROM user_data " \
              "WHERE ID=?"
        self.cur.execute(sql, (user_id,))
        result = self.cur.fetchone()
        num = result[0]
        return num


if __name__ == "__main__":
    # db = Datastore()
    # db.addGuild(123)
    # db.addGuild(234)
    # db.addDeafenTrack(123, 234)
    # db.addDeafenTrack(123, 345)
    # db.removeDeafenTrack(123, 234)
    # db.addDeafenData(234)
    # print(db.getGuildIDS())
    # print(db.getUserIDS())
    # print(db.getDeafenTracks())
    # print(db.getDeafenTracksINV())
    # print(db.getDeafenData(234))

    db = Datastore()
    print(db.getGuildIDS())
    print(db.getUserIDS())
