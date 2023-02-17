class DeafenMemory:
    def __init__(self, user_map: dict, time_limit: int = 60):

        # (last_time, last_time_marked, guild_ids)
        self.user_map = {user_id: (None, None, guild_ds) for user_id, guild_ds in user_map.items()}

        self.time_limit = time_limit

    @property
    def users(self):
        return self.user_map.keys()

    def markDeafen(self, deafen_ids: list[int], time):
        """

        :param deafen_ids:
        :param time:
        :return: {user_id: {guild_ids}}
        """
        mark_ids = dict()

        for user_id, (last_time, last_time_marked, guild_ids) in self.user_map.items():
            # If user is found deafen
            if user_id in deafen_ids:

                # If deafened user, first time deafened, then mark
                if last_time is None:

                    # last time
                    self.user_map[user_id] = (time, None, guild_ids)

                # If deafened user: exceeded time limit (make sure that last_time_marked does not match), then flag user
                elif last_time_marked != last_time and time - last_time >= self.time_limit:

                    # Mark last time
                    self.user_map[user_id] = (last_time, last_time, guild_ids)

                    # Return user id data
                    mark_ids[user_id] = guild_ids

            # If user not deafen, reset timers
            else:
                self.user_map[user_id] = (None, None, guild_ids)

        return mark_ids

    def addUser(self, guild_id: int, user_id: int):
        if user_id in self.user_map:
            (last_time, last_time_marked, guild_ids) = self.user_map[user_id]
            guild_ids.add(guild_id)
            self.user_map[user_id] = (last_time, last_time_marked, guild_ids)
        else:
            self.user_map[user_id] = (None, None, {guild_id})

    def removeUser(self, guild_id: int, user_id: int):
        if user_id in self.user_map:
            (last_time, last_time_marked, guild_ids) = self.user_map[user_id]
            guild_ids.remove(guild_id)
            self.user_map[user_id] = (last_time, last_time_marked, guild_ids)
