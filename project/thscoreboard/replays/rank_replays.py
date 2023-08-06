from replays import models
from replays.models import ReplayQuerySet


def add_global_rank_annotations(replays: ReplayQuerySet) -> ReplayQuerySet:
    """Ranks replays in the replay query set against all ranked replays"""
    top_3_replays = (
        models.Replay.objects.filter(category=models.Category.STANDARD)
        .filter(replay_type=1)
        .filter(is_listed=True)
        .annotate_with_rank()
        .filter(rank__lte=3)
        .all()
    )
    rank_dict = {replay.id: replay.rank for replay in top_3_replays}

    for replay in replays:
        replay.rank = rank_dict.get(replay.id, -1)

    return replays
