from MySQL_Driver import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("Func_file_error")
logger_func = logging.getLogger("Func_file")


def AddNewProfile(CID, UID, UNickName):
    MV = 0
    set = ParseUserSettings(UID)
    try:
        executeSQL(
            "INSERT INTO `Main` (`ChannelID`, `UserID`, `UserNickname`) "
            f"VALUES ('{CID}', '{UID}', '{UNickName}');")
    except Exception as e:
        logger.exception(f"Виникла помилка в функції AddNewProfile(Main). DEBUG:\nException: {e}")
        return False
    finally:
        DBCommit()
    for x in set:
        print(f"x[0]: {x[0]}")
        print(f" UID: {UID}")
        if str(x[0]) == str(UID):
            MV = 1
    if MV > 0:
        print("TRUE")
        return True
    else:
        print("FALSE")
    try:
        executeSQL(
            "INSERT INTO `Settings` (`UserID`, `State`, `TimeWhenPing`, `ReloadTime`, `DNDM`, `DNDM_Time`) "
            f"VALUES ('{UID}', '1', '0', '60', '0', '0');")
    except Exception as e:
        logger.exception(f"Виникла помилка в функції AddNewProfile(Settings). DEBUG:\nException: {e}")
        return False
    finally:
        DBCommit()
    return True


def CheckAllUserChannels(UID):
    try:
        info = executeSQL(f"SELECT ChannelID from Main WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції CheckAllUserChannels. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserInfo(UID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserInfoC(UID, CID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE UserID={UID} AND ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserSettings(UID):
    try:
        info = executeSQL(f"SELECT * from Settings WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserSettings. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    print(f"IFFO: {info}")
    return info


def ParseAllUsers(CID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserSettings. DEBUG:\n ChannelID: {CID}\nException: {e}")
        return False
    print(f"ParseAllUsers: {info}")
    return info


def ChangeNick(UID, NewNick):
    try:
        info = sendSQL(f"UPDATE Main SET UserNickname='{NewNick}' WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції ChangeNick. DEBUG:\n UserID: {UID}\n param: {NewNick}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"ChangeNick: {info}")
    return True


# Settings DEfs
def StateSettings(UID, param):
    try:
        info = sendSQL(f"UPDATE Settings SET State={param} WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції StateSetting. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"StateSet: {info}")
    return True


def TWPSettings(UID, param):
    try:
        info = sendSQL(f"UPDATE Settings SET TimeWhenPing={param} WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції TWPSettings. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"TWPSettings: {info}")
    return True


def RTSettings(UID, param):
    try:
        info = sendSQL(f"UPDATE Settings SET ReloadTime={param} WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції RTSettings. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"ReloadTime: {info}")
    return True


def DNDMSettings(UID, param):
    try:
        info = sendSQL(f"UPDATE Settings SET DNDM={param} WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції DNDMSettings. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"DNDMSettings: {info}")
    return True


def DNDMTSettings(UID, param):
    try:
        info = sendSQL(f"UPDATE Settings SET DNDM_Time={param} WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції DNDMTSettings. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"DNDMTSettings: {info}")
    return True
def LPTSettings(CID, UID, param):
    try:
        info = sendSQL(f"UPDATE Main SET LastPingTime='{param}' WHERE UserID={UID} AND ChannelID={CID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції LPTSettings. DEBUG:\n UserID: {UID}\n param: {param}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"LPTSettings: {info}")
    return True

def TTS(T1, T2):
    t1 = T1.split(":")
    t2 = T2.split(":")
    print(f"T1: {t1}   T2:{t2}")
    H1 = int(t1[0])
    M1 = int(t1[1])
    S1 = int(t1[2])
    H2 = int(t2[0])
    M2 = int(t2[1])
    S2 = int(t2[2])
    alls1 = (((H1*60)*60)+(M1*60)+S1)
    alls2 = (((H2*60)*60)+(M2*60)+S2)
    return alls1-alls2

