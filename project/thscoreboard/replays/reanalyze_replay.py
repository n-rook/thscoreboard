"""Recompute facts about a replay from its replay file.

This module is useful when updates are made to the site, allowing new
information to be derived from existing replay files.

As this module is used only for administrative work, it is not optimized
for speed.
"""

import copy
from typing import Optional

from django.db import models as django_models

from replays import game_ids
from replays import models
from replays import replay_parsing


def CheckReplay(replay_id: int) -> str:
    """Check a replay and return information about how it would be updated."""

    replay = models.Replay.objects.get(id=replay_id)
    replay_file = models.ReplayFile.objects.get(replay=replay)
    replay_info = replay_parsing.Parse(replay_file.replay_file)
    replay_to_update = copy.deepcopy(replay)
    replay_diffs = []

    replay_to_update.SetFromReplayInfo(replay_info)
    replay_diffs.append(_Diff(replay, replay_to_update))

    replay_stages = models.ReplayStage.objects.filter(replay=replay_id).order_by('stage')
    seen_stages = set()
    for replay_file_stage_info in replay_info.stages:
        matching_stages = [r for r in replay_stages
                           if r.stage == replay_file_stage_info.stage]

        if len(matching_stages) > 1:
            raise AssertionError(
                f'{len(matching_stages)} matching stages; this is impossible')
        elif len(matching_stages) == 1:
            seen_stages.add(replay_file_stage_info.stage)
            matching_stage = matching_stages[0]
            matching_stage_to_update = copy.deepcopy(matching_stage)
            matching_stage_to_update.SetFromReplayStageInfo(replay_file_stage_info)
            stage_diff = _Diff(matching_stage, matching_stage_to_update)
        else:
            # TODO: Deduplicate this with the real logic in create_replay.py somehow.
            new_stage = models.ReplayStage(
                replay=replay,
                stage=replay_file_stage_info.stage
            )
            if replay_info.game == game_ids.GameIDs.TH09:
                new_stage.th09_p2_shot = models.Shot.objects.select_related('game').get(game=game_ids.GameIDs.TH09, shot_id=replay_file_stage_info.th09_p2_shot)
            new_stage.SetFromReplayStageInfo(replay_file_stage_info)
            stage_diff = _Diff(None, new_stage)

        if stage_diff:
            stage_diff = f'Stage {replay_file_stage_info.stage}:\n' + stage_diff
            replay_diffs.append(stage_diff)
    for replay_stage in replay_stages:
        if replay_stage.stage not in seen_stages:
            stage_diff = f'Stage {replay_stage.stage}:\n' + _Diff(replay_stage, None)
            replay_diffs.append(stage_diff)

    return '\n\n'.join([d for d in replay_diffs if d])


def _GetComparableFields(m: django_models.Model):
    return [
        f for f in m._meta.get_fields()
        # TODO: This should really return some relations, just not all of them.
        if not f.is_relation
    ]


def _Diff(old_model: Optional[django_models.Model], new_model: Optional[django_models.Model]) -> str:
    diff = []

    if old_model is None and new_model is None:
        pass  # Do nothing; just return empty string
    if old_model is None:
        for f in _GetComparableFields(new_model):
            diff.append('[{field}] (No model!) -> {new}'.format(
                field=f.name, new=f.value_to_string(new_model)
            ))
    elif new_model is None:
        for f in _GetComparableFields(old_model):
            diff.append('[{field}] {old} -> (No model!)'.format(
                field=f.name, old=f.value_to_string(old_model)
            ))
    else:
        for f in _GetComparableFields(old_model):
            old_value = f.value_to_string(old_model)
            new_value = f.value_to_string(new_model)
            if old_value != new_value:
                diff.append('[{field}] {old} -> {new}'.format(
                    field=f.name,
                    old=old_value,
                    new=new_value
                ))
    return '\n'.join(diff)
