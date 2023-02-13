import time

import datastore
import memory

db = datastore.Database()
dm = memory.DeafenMemory(db.getDeafenTracks())


def convert_from_ms(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = seconds + milliseconds / 1000
    return days, hours, minutes, seconds


def ms_to_str(milliseconds):
    days, hours, minutes, seconds = convert_from_ms(milliseconds)
    if days:
        return f"{days} days {hours} hrs {minutes} minutes {seconds} seconds"
    elif hours:
        return f"{hours} hrs {minutes} minutes {seconds} seconds"
    elif minutes:
        return f"{minutes} minutes {seconds} seconds"
    elif seconds:
        return f"{seconds} seconds"
    return milliseconds


def flipDictionary(d: dict):
    ret_d = dict()
    for key, value in d.items():
        for item in value:
            if item in ret_d:
                ret_d[item].add(key)
            else:
                ret_d[item] = {key}
    return ret_d


def getTrackedDeafenUsers():
    return dm.users


def updateDeafenUsers(user_ids):
    """
    :param user_ids: The deafened user ids
    :return: {guild_id: {user_ids}}
    """
    deafen_user_dict = dm.markDeafen(user_ids, time.time())  # {user_id: {guild_ids}}

    # Update database to track user deafen counts
    for user_id in deafen_user_dict:
        db.addDeafenData(user_id)
    db.commit()

    return flipDictionary(deafen_user_dict)


def addDeafenTrack(guild_id: int, user_id: int):
    db.addDeafenTrack(guild_id, user_id)
    dm.addUser(guild_id, user_id)
    db.commit()


def removeDeafenTrack(guild_id: int, user_id: int):
    db.removeDeafenTrack(guild_id, user_id)
    dm.removeUser(guild_id, user_id)
    db.commit()


def getDeafenData(user_id: int):
    return db.getDeafenData(user_id)
