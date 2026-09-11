meta:
  id: th03_v14
  file-extension: rpy
  endian: le
seq:
  - id: magic
    contents: T3RPLY14
  - id: version
    type: u2
    valid: 14
  - id: header_size
    type: u2
    valid: 896
  - id: sample_size
    type: u2
    valid: 0
  - id: flags
    type: u2
  - id: status
    type: u1
  - id: end_reason
    type: u1
  - id: game_mode
    type: u1
  - id: rank
    type: u1
  - id: key_mode
    type: u1
  - id: playchar_p1
    type: u1
  - id: playchar_p2
    type: u1
  - id: story_stage
    type: u1
  - id: is_cpu_p1
    type: u1
  - id: is_cpu_p2
    type: u1
  - id: sample_count
    type: u4
  - id: final_frame_count
    type: u4
  - id: resident_rand
    type: u4
  - id: random_seed_snapshot
    type: u4
  - id: input_offset
    type: u4
  - id: input_size
    type: u4
  - id: snapshot_offset
    type: u4
    valid: 896
  - id: snapshot_size
    type: u4
    valid: 289
  - id: summary_flags
    type: u2
  - id: final_route
    type: u1
  - id: final_game_mode
    type: u1
  - id: final_story_stage
    type: u1
  - id: final_round_id
    type: u1
  - id: final_winner
    type: u1
  - id: final_story_lives
    type: u1
  - id: final_misses
    type: u1
  - id: stage_reached_count
    type: u1
  - id: story
    type: story_summary
    if: (flags & 4) == 0
  - id: practice
    type: practice_summary
    if: (flags & 4) != 0
  - id: final_score
    type: packed_score
  - id: autofire
    type: u1
  - id: dos_date
    type: u2
  - id: name
    size: 8
  - id: summary
    type: summary_extension
  - id: ruleset
    type: u1
  - id: recording_flags
    type: u1
  - id: recorder_role
    type: u1
  - id: recorder_source
    type: u1
  - id: player_one_uuid
    size: 16
  - id: player_two_uuid
    size: 16
  - id: match_id
    size: 16
  - id: player_one_nametag_length
    type: u1
    valid:
      max: 57
  - id: player_two_nametag_length
    type: u1
    valid:
      max: 57
  - id: player_one_nametag
    size: 57
  - id: player_two_nametag
    size: 57
  - id: identity_reserved
    size: 106
  - id: checkpoints
    type: checkpoint
    repeat: expr
    repeat-expr: (input_offset - header_size) / snapshot_size
  - id: input
    size: input_size
types:
  packed_score:
    seq:
      - id: digits
        size: 4
  story_summary:
    seq:
      - id: stage_opponents
        type: u1
        repeat: expr
        repeat-expr: 9
      - id: stage_scores
        type: packed_score
        repeat: expr
        repeat-expr: 9
  practice_summary:
    seq:
      - id: preset
        type: u1
      - id: stage
        type: u1
      - id: round
        type: u1
      - id: stock
        type: u1
      - id: extends_gained
        type: u1
      - id: cpu_timer
        type: u1
      - id: round_speed
        type: u1
      - id: bullet_speed
        type: u1
      - id: p1_spell
        type: u1
      - id: cpu_spell
        type: u1
      - id: boss_level
        type: u1
      - id: cpu_damage
        type: u1
      - id: initial_cpu_safety_frames
        type: u2
      - id: p1_gauge
        type: u1
      - id: cpu_gauge
        type: u1
      - id: reserved
        size: 29
  round_split:
    seq:
      - id: stage_round
        type: u1
      - id: route_winner
        type: u1
      - id: score_p1
        type: packed_score
      - id: score_p2
        type: packed_score
      - id: real_frames
        type: u4
  stage_clear_bonus:
    seq:
      - id: total
        type: packed_score
      - id: max_combo
        type: u1
      - id: gauge_attacks
        type: u1
      - id: boss_attacks
        type: u1
      - id: boss_reversals
        type: u1
      - id: boss_panics
        type: u1
      - id: remaining_lives
        type: u1
  checkpoint:
    seq:
      - id: sample_count
        type: u4
      - id: global_frame
        type: u4
      - id: input_size
        type: u4
      - id: snapshot
        type: compact_snapshot
      - id: round_state
        type: round_state
      - id: round_carry
        size: 163
  compact_snapshot:
    seq:
      - id: resident_rand
        type: u4
      - id: random_seed_snapshot
        type: u4
      - id: rank
        type: u1
      - id: key_mode
        type: u1
      - id: game_mode
        type: u1
      - id: story_stage
        type: u1
      - id: story_lives
        type: u1
      - id: rem_credits
        type: u1
      - id: skill
        type: u1
      - id: demo_num
        type: u1
      - id: pid_winner
        type: u1
      - id: show_score_menu
        type: u1
      - id: op_animation_fast
        type: u1
      - id: is_cpu
        type: u1
        repeat: expr
        repeat-expr: 2
      - id: playchar_paletted
        type: u1
        repeat: expr
        repeat-expr: 2
      - id: story_opponents
        type: u1
        repeat: expr
        repeat-expr: 9
      - id: score_last
        type: unpacked_score
        repeat: expr
        repeat-expr: 2
      - id: autofire
        type: u1
      - id: player_runtime
        size: 30
      - id: round_reset_seed
        type: u4
      - id: formation_first
        type: u1
  unpacked_score:
    seq:
      - id: digits
        size: 8
  round_state:
    seq:
      - id: round_id
        type: u1
      - id: rounds_won
        type: u1
        repeat: expr
        repeat-expr: 2
      - id: score
        type: unpacked_score
        repeat: expr
        repeat-expr: 2
      - id: round_speed
        type: u1
      - id: bullet_speed
        type: u1
      - id: spell_rank
        type: u1
        repeat: expr
        repeat-expr: 2
      - id: boss_rank
        type: u1
      - id: cpu_damage
        type: u1
      - id: extends_gained
        type: u1
      - id: cpu_safety_frames
        type: u2
        repeat: expr
        repeat-expr: 2
  summary_extension:
    seq:
      - id: flags
        type: u1
      - id: round_reached_count
        type: u1
      - id: round_splits
        type: round_split
        repeat: expr
        repeat-expr: 27
      - id: stage_clear_bonuses
        type: stage_clear_bonus
        repeat: expr
        repeat-expr: 9
      - id: timed_frames
        type: u4
      - id: slow_frames
        type: u4
      - id: checkpoint_count
        type: u1
      - id: checkpoint_stage_round
        type: u1
        repeat: expr
        repeat-expr: 15
