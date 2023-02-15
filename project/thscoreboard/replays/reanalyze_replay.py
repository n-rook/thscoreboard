"""Recompute facts about a replay from its replay file.

This module is useful when updates are made to the site, allowing new
information to be derived from existing replay files.

As this module is used only for administrative work, it is not optimized
for speed.
"""

import abc
import copy
from typing import Optional

from django.db import models as django_models
from django.db import transaction

from replays import game_ids
from replays import models
from replays import replay_parsing


def DoesReplayNeedUpdate(replay_id: int) -> str:
    """Return whether a replay would be updated."""
    return bool(CheckReplay(replay_id))


def CheckReplay(replay_id: int) -> str:
    """Check a replay and return information about how it would be updated."""

    differ = _Differ()
    _Reanalyze(replay_id, differ)
    return differ.GetOutput()


@transaction.atomic
def UpdateReplay(replay_id: int) -> None:
    """Update a replay by recomputing its derived fields."""
    updater = _Updater()
    _Reanalyze(replay_id, updater)


class _Recorder(abc.ABC):
    """Internal class that records a difference that happened during reanalysis."""

    @abc.abstractmethod
    def Change(self, name: str, old_model: django_models.Model, new_model: django_models.Model):
        """Record a change to a row."""

    @abc.abstractmethod
    def New(self, name: str, new_model: django_models.Model):
        """Record a new row."""

    @abc.abstractmethod
    def Deleted(self, name: str, old_model: django_models.Model):
        """Record a row being deleted."""


class _Differ(_Recorder):
    """A Differ just records changes in text."""

    def __init__(self) -> None:
        super().__init__()
        self._output = []

    def _PrefaceWithName(self, name, diff_str):
        if not diff_str:
            # Don't preface the empty string.
            return ''
        return f'{name}:\n{diff_str}'

    def Change(self, name: str, old_model: django_models.Model, new_model: django_models.Model):
        diff = _Diff(old_model, new_model)
        if diff:
            self._output.append(self._PrefaceWithName(name, diff))

    def New(self, name: str, new_model: django_models.Model):
        diff = _Diff(None, new_model)
        if diff:
            self._output.append(self._PrefaceWithName(name, diff))

    def Deleted(self, name: str, old_model: django_models.Model):
        diff = _Diff(old_model, None)
        if diff:
            self._output.append(self._PrefaceWithName(name, diff))

    def GetOutput(self):
        return '\n\n'.join([d for d in self._output if d])


class _Updater(_Recorder):
    """A Differ that actually makes changes to an update."""

    def Change(self, name: str, old_model: django_models.Model, new_model: django_models.Model):
        new_model.save()

    def New(self, name: str, new_model: django_models.Model):
        new_model.save()

    def Deleted(self, name: str, old_model: django_models.Model):
        old_model.delete()


def _Reanalyze(replay_id: int, recorder: _Recorder) -> str:
    """Reanalyze computed fields on a replay."""

    replay = models.Replay.objects.get(id=replay_id)
    replay_file = models.ReplayFile.objects.get(replay=replay)
    replay_info = replay_parsing.Parse(replay_file.replay_file)
    replay_to_update = copy.deepcopy(replay)

    replay_to_update.SetFromReplayInfo(replay_info)
    recorder.Change('Replay', replay, replay_to_update)

    replay_stages = models.ReplayStage.objects.filter(replay=replay_id).order_by('stage')
    seen_stages = set()
    for replay_file_stage_info in replay_info.stages:
        matching_stages = [r for r in replay_stages
                           if r.stage == replay_file_stage_info.stage]
        stage_name = f'Stage {replay_file_stage_info.stage + 1}'

        if len(matching_stages) > 1:
            raise AssertionError(
                f'{len(matching_stages)} matching stages; this is impossible')
        elif len(matching_stages) == 1:
            seen_stages.add(replay_file_stage_info.stage)
            matching_stage = matching_stages[0]
            matching_stage_to_update = copy.deepcopy(matching_stage)
            matching_stage_to_update.SetFromReplayStageInfo(replay_file_stage_info)
            recorder.Change(stage_name, matching_stage, matching_stage_to_update)
        else:
            # TODO: Deduplicate this with the real logic in create_replay.py somehow.
            new_stage = models.ReplayStage(
                replay=replay,
                stage=replay_file_stage_info.stage
            )
            if replay_info.game == game_ids.GameIDs.TH09:
                new_stage.th09_p2_shot = models.Shot.objects.select_related('game').get(game=game_ids.GameIDs.TH09, shot_id=replay_file_stage_info.th09_p2_shot)
            new_stage.SetFromReplayStageInfo(replay_file_stage_info)
            recorder.New(stage_name, new_stage)

    for replay_stage in replay_stages:
        if replay_stage.stage not in seen_stages:
            recorder.Deleted(f'Stage {replay_stage.stage + 1}', replay_stage)


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
    elif old_model is None:
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
