"""A class that provides methods used to properly format and display replay data"""

import copy
from immutabledict import immutabledict
from . import game_ids

_table_fields_th06 = immutabledict({
    'stage': True,
    'score': True,
    'piv': False,
    'graze': False,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': True,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
})

_table_fields_th07 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': True,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': True,
    'th07_cherrymax': True,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
})

_table_fields_th08 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': True,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
})

_table_fields_th09 = immutabledict({
    'stage': True,
    'score': True,
    'piv': False,
    'graze': False,
    'point_items': False,
    'power': False,
    'lives': True,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': True,
    'th09_p2_cpu': True,
    'th09_p2_shot': True,
    'th09_p2_score': True,
})

_table_fields_th10 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': False,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
})

_table_fields_th11 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': True,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
})

_game_fields = immutabledict({
    'th01': None,
    'th05': None,
    'th06': _table_fields_th06,
    'th07': _table_fields_th07,
    'th08': _table_fields_th08,
    'th09': _table_fields_th09,
    'th10': _table_fields_th10,
    'th11': _table_fields_th11
})


def GetFormatPower(game_id: str, power: int) -> str:
    if power is None:
        return ""
    if game_id in (game_ids.GameIDs.TH06, game_ids.GameIDs.TH07, game_ids.GameIDs.TH08):
        return str(power)
    if game_id in (game_ids.GameIDs.TH10, game_ids.GameIDs.TH11):
        return "%.2f" % (float(power) * 0.05)

    return str(power)


_life_pieces = immutabledict({
    'th01': None,
    'th05': None,
    'th06': None,
    'th07': None,
    'th08': None,
    'th09': None,
    'th10': None,
    'th11': 5
})


def GetFormatLives(game_id: str, lives: int, life_pieces: int) -> str:
    if lives is None:
        return ""
    total_life_pieces = _life_pieces[game_id]
    if total_life_pieces is None:
        return str(lives)
    else:
        return f"{lives} ({life_pieces}/{total_life_pieces})"


def GetGameField(gameid: str):
    if gameid in _game_fields:
        return _game_fields[gameid]
    return None


def GetGameLifePieces(gameid: str):
    if gameid in _life_pieces:
        return _life_pieces[gameid]
    return None


def GetFormatStage(game_id: str, stage: int) -> str:
    if stage is None:
        return ""
    if game_id == "th08":
        stages = {
            0: '1',
            1: '2',
            2: '3',
            3: '4A',
            4: '4B',
            5: '5',
            6: '6A',
            7: '6B',
            8: '7',
        }
        return stages[stage]
    elif game_id in ['th06', 'th07', 'th09']:
        return str(stage + 1)
    else:
        return str(stage)


def FormatStages(game_id: str, replay_stages):
    """This function formats the stage values to be displayed in the front end"""
    new_stages = copy.deepcopy(replay_stages)

    for stage in new_stages:
        stage.power = GetFormatPower(game_id, stage.power)
        stage.stage = GetFormatStage(game_id, stage.stage)
        stage.lives = GetFormatLives(game_id, stage.lives, stage.life_pieces)
        if game_id == game_ids.GameIDs.TH09:
            stage.th09_p2_shotFormat = stage.th09_p2_shot.GetName()

        if stage.stage is None:
            stage.stage = ""
        if stage.score is None:
            stage.score = ""
        if stage.piv is None:
            stage.piv = ""
        if stage.graze is None:
            stage.graze = ""
        if stage.point_items is None:
            stage.point_items = ""
        if stage.power is None:
            stage.power = ""
        if stage.lives is None:
            stage.lives = ""
        if stage.life_pieces is None:
            stage.life_pieces = ""
        if stage.bombs is None:
            stage.bombs = ""
        if stage.bomb_pieces is None:
            stage.bomb_pieces = ""
        if stage.th06_rank is None:
            stage.th06_rank = ""
        if stage.th07_cherry is None:
            stage.th07_cherry = ""
        if stage.th07_cherrymax is None:
            stage.th07_cherrymax = ""
        if stage.th09_p1_cpu is None:
            stage.th09_p1_cpu = ""
        if stage.th09_p2_cpu is None:
            stage.th09_p2_cpu = ""
        if stage.th09_p2_score is None:
            stage.th09_p2_score = ""
    
    return new_stages
