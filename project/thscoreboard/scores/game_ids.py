"""Various human-readable game IDs, used in low-level libraries like game_ids.py."""


class GameIDs:
    TH05 = 'th05'
    TH06 = 'th06'


def GetGameName(game_id: str, short=False):
    if game_id == GameIDs.TH05:
        if short:
            return 'th05'
        else:
            return '東方怪綺談 - Mystic Square'
    if game_id == GameIDs.TH06:
        if short:
            return 'th06'
        else:
            return '東方紅魔郷 - Embodiment of Scarlet Devil'
    return 'Unknown game (bug!)'


def GetShotName(game_id: str, shot_id: str):
    if game_id == GameIDs.TH05:
        # The names are the same as the short codenames.
        # Well, in English.
        return shot_id
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
    if game_id in {GameIDs.TH05, GameIDs.TH06}:
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
