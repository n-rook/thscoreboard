"""Various human-readable game IDs, used in low-level libraries like game_ids.py."""


from telnetlib import GA


class GameIDs:
    TH06 = 'th06'


def GetGameName(game_id: str):
    if game_id == GameIDs.TH06:
        return '東方紅魔郷 - Embodiment of Scarlet Devil'
    return 'Unknown game (bug!)'


def GetShotName(game_id: str, shot_id: str):
    if game_id == GameIDs.TH06:
        if shot_id == 'ReimuA':
            return 'Reimu A'
        elif shot_id == 'ReimuB':
            return 'Reimu B'
        elif shot_id == 'MarisaA':
            return 'Marisa A'
        elif shot_id == 'MarisaB':
            return 'Marisa B'
    return 'Bug shot'


def GetDifficultyName(game_id: str, difficulty: int):
    if game_id == GameIDs.TH06:
        if difficulty == 0:
            return 'Easy'
        elif difficulty == 1:
            return 'Normal'
        elif difficulty == 2:
            return 'Hard'
        elif difficulty == 3:
            return 'Lunatic'
        elif difficulty == 4:
            return 'Extra'
    
    return 'Bug difficulty'

# TH06_SHOT_NAME_TO_ID_BIDICT = bidict({
#     'ReimuA': 0,
#     'ReimuB': 1,
#     'MarisaA': 2,
#     'MarisaB': 3,
# })
# """Map shot types to database-ready numeric IDs."""