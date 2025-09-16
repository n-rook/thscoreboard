"""A class that provides methods used to properly format and display replay data"""

import copy
from immutabledict import immutabledict
from typing import Iterable, Optional
from . import game_ids
from replays import models

#   These table fields configure the display of the stage split columns
#   These may differ from whether the replay file actually has the field or not
#       depending on whether it is relevant to show that field
#   eg. life_pieces will almost always be False as displaying it is integrated into Lives

_table_fields_th06 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": False,
        "graze": False,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": True,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th07 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": True,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": True,
        "th07_cherrymax": True,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th08 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": True,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th09 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": False,
        "graze": False,
        "point_items": False,
        "power": False,
        "lives": True,
        "bombs": False,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": True,
        "th09_p2_score": True,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th09_PVP = immutabledict(
    {
        "stage": True,
        "score": False,
        "piv": False,
        "graze": False,
        "point_items": False,
        "power": False,
        "lives": False,
        "bombs": False,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": True,
        "th09_p2_cpu": True,
        "th09_p2_shot": True,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th10 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": False,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": False,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th11 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": False,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th12 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th13 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": True,
        "th16_season_power": False,
        "extends": True,
    }
)

_table_fields_th14 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th15 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th16 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": True,
        "extends": False,
    }
)

_table_fields_th17 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th18 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": True,
        "graze": True,
        "point_items": False,
        "power": True,
        "lives": True,
        "bombs": True,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": False,
        "th128_perfect_freeze": False,
        "th128_frozen_area": False,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_table_fields_th128 = immutabledict(
    {
        "stage": True,
        "score": True,
        "piv": False,
        "graze": True,
        "point_items": False,
        "power": False,
        "lives": False,
        "bombs": False,
        "th06_rank": False,
        "th07_cherry": False,
        "th07_cherrymax": False,
        "th09_p1_cpu": False,
        "th09_p2_cpu": False,
        "th09_p2_shot": False,
        "th09_p2_score": False,
        "th128_motivation": True,
        "th128_perfect_freeze": True,
        "th128_frozen_area": True,
        "th13_trance": False,
        "th16_season_power": False,
        "extends": False,
    }
)

_game_fields = immutabledict(
    {
        "th01": None,
        "th05": None,
        "th06": _table_fields_th06,
        "th07": _table_fields_th07,
        "th08": _table_fields_th08,
        "th09": _table_fields_th09,
        "th10": _table_fields_th10,
        "th11": _table_fields_th11,
        "th12": _table_fields_th12,
        "th128": _table_fields_th128,
        "th13": _table_fields_th13,
        "th14": _table_fields_th14,
        "th15": _table_fields_th15,
        "th16": _table_fields_th16,
        "th17": _table_fields_th17,
        "th18": _table_fields_th18,
    }
)

_game_fields_PVP = immutabledict(
    {
        "th01": None,
        "th05": None,
        "th06": None,
        "th07": None,
        "th08": None,
        "th09": _table_fields_th09_PVP,
        "th10": None,
        "th11": None,
        "th12": None,
        "th128": None,
        "th13": None,
        "th14": None,
        "th15": None,
        "th16": None,
        "th17": None,
        "th18": None,
    }
)


def GetFormatPower(
    game_id: str, power: Optional[int], shot: Optional[str] = None
) -> str:
    if power is None:
        return ""
    if game_id in (game_ids.GameIDs.TH06, game_ids.GameIDs.TH07, game_ids.GameIDs.TH08):
        return str(power)
    if game_id == game_ids.GameIDs.TH11 and shot == "MarisaA":
        return "%.2f" % round(float(power) / 12, ndigits=2)
    if game_id in (game_ids.GameIDs.TH10, game_ids.GameIDs.TH11):
        return "%.2f" % (float(power) * 0.05)
    if game_id in (
        game_ids.GameIDs.TH12,
        game_ids.GameIDs.TH13,
        game_ids.GameIDs.TH14,
        game_ids.GameIDs.TH15,
        game_ids.GameIDs.TH16,
        game_ids.GameIDs.TH17,
        game_ids.GameIDs.TH18,
    ):
        return "{:.2f}".format(power / 100)

    return str(power)


# used in GetFormatLives for string formatting the life/life piece counts
# if this is None, lives will be displayed standalone instead of including the life piece counts
# Technically the maximum life pieces for TH12 is 5, but the first piece you collect gives you 2, so functionally there are only 4
#   The parser for the game accounts for this discrepancy
_life_pieces = immutabledict(
    {
        "th01": None,
        "th02": None,
        "th03": None,
        "th04": None,
        "th05": None,
        "th06": None,
        "th07": None,
        "th08": None,
        "th09": None,
        "th10": None,
        "th11": 5,
        "th12": 4,
        "th128": None,
        "th13": None,  # this game has variable life pieces, so hardcoding it doesn't work
        "th14": 3,
        "th15": 3,
        "th16": None,
        "th17": 3,
        "th18": 3,
    }
)


# used in GetFormatBombs for string formatting the bomb/bomb piece counts
_bomb_pieces = immutabledict(
    {
        "th01": None,
        "th02": None,
        "th03": None,
        "th04": None,
        "th05": None,
        "th06": None,
        "th07": None,
        "th08": None,
        "th09": None,
        "th10": None,
        "th11": None,
        "th12": 3,
        "th128": None,
        "th13": 8,
        "th14": 8,
        "th15": 5,
        "th16": 5,
        "th17": 3,
        "th18": 3,
    }
)


# Takes the lives and life pieces and formats them accordingly for viewing in frontend
# A special case is made here for TH13, since it has a variable number of life pieces needed
#   so the amount is calculated off of the current extends
def GetFormatLives(
    game_id: str,
    lives: Optional[int],
    life_pieces: Optional[int],
    extends: Optional[int] = 0,
) -> str:
    if lives is None:
        return ""

    life_pieces_str = ""

    if game_id == "th13":
        threshholds = [8, 10, 12, 15, 18, 20, 25]
        if extends is None:
            life_pieces_str = ""
        else:
            if extends > 5:
                extends = 6
            if extends < 0:
                extends = 0
            life_pieces_str = f" ({life_pieces}/{threshholds[extends]})"
    else:
        total_life_pieces = _life_pieces[game_id]
        if total_life_pieces is None:
            life_pieces_str = ""
        else:
            if life_pieces is None:
                life_pieces = 0
            life_pieces_str = f" ({life_pieces}/{total_life_pieces})"
    return f"{lives}{life_pieces_str}"


def GetFormatBombs(
    game_id: str, bombs: Optional[int], bomb_pieces: Optional[int]
) -> str:
    if bombs is None:
        return ""
    total_bomb_pieces = _bomb_pieces[game_id]
    if total_bomb_pieces is None:
        return str(bombs)
    else:
        if bomb_pieces is None:
            bomb_pieces = 0
        return f"{bombs} ({bomb_pieces}/{total_bomb_pieces})"


def GetGameField(gameid: str, replay_type: game_ids.ReplayTypes):
    if replay_type is game_ids.ReplayTypes.PVP:
        if gameid in _game_fields_PVP:
            return _game_fields_PVP[gameid]
    else:
        if gameid in _game_fields:
            return _game_fields[gameid]
    return None


FORMAT_EXTRA = "Extra"
FORMAT_PHANTASM = "Phantasm"


def GetFormatStage(game_id: str, stage: Optional[int]) -> str:
    if stage is None:
        return ""
    if game_id == "th08":
        stages = {
            1: "1",
            2: "2",
            3: "3",
            4: "4A",
            5: "4B",
            6: "5",
            7: "6A",
            8: "6B",
            9: FORMAT_EXTRA,
        }
        return stages[stage]
    if game_id == "th09":
        if stage == 10:
            return FORMAT_EXTRA
    elif game_id == "th07" and stage == 8:
        return FORMAT_PHANTASM
    elif game_id == "th128":
        stages = {
            1: "A1-1",
            2: "A1-2",
            3: "A1-3",
            4: "A2-2",
            5: "A2-3",
            6: "B1-1",
            7: "B1-2",
            8: "B1-3",
            9: "B2-2",
            10: "B2-3",
            11: "C1-1",
            12: "C1-2",
            13: "C1-3",
            14: "C2-2",
            15: "C2-3",
            16: "Extra",
        }
        return stages[stage]
    elif stage == 7:
        return FORMAT_EXTRA
    return str(stage)


def FormatStages(game_id: str, replay_stages: Iterable[models.ReplayStage], shot: str):
    """This function formats the stage values to be displayed in the front end"""
    new_stages = copy.deepcopy(replay_stages)

    for stage in new_stages:
        stage.power = GetFormatPower(game_id, stage.power, shot)
        stage.stage = GetFormatStage(game_id, stage.stage)
        stage.lives = GetFormatLives(
            game_id, stage.lives, stage.life_pieces, stage.extends
        )
        stage.bombs = GetFormatBombs(game_id, stage.bombs, stage.bomb_pieces)
        if game_id == game_ids.GameIDs.TH09:
            stage.th09_p2_shotFormat = stage.th09_p2_shot.GetName()

        if stage.th128_motivation is None:
            stage.th128_motivation = ""
        else:
            stage.th128_motivation = f"{stage.th128_motivation//100}%"

        if stage.th128_perfect_freeze is None:
            stage.th128_perfect_freeze = ""
        else:
            stage.th128_perfect_freeze = f"{stage.th128_perfect_freeze//100}%"

        if stage.th128_frozen_area is None:
            stage.th128_frozen_area = ""
        else:
            stage.th128_frozen_area = f"{int(stage.th128_frozen_area)}%"

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
        if stage.bombs is None:
            stage.bombs = ""
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
        if stage.th13_trance is None:
            stage.th13_trance = ""
        else:
            stage.th13_trance = (
                f"{stage.th13_trance//200} + {stage.th13_trance%200}/200"
            )
        if stage.th16_season_power is None:
            stage.th16_season_power = ""
        if stage.extends is None:
            stage.extends = ""

    return new_stages


_games_with_pvp = ["th03", "th09"]


def game_has_pvp(game_id: str) -> bool:
    return game_id in _games_with_pvp
