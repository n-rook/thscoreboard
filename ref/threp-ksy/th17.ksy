meta:
  id: th17
  file-extension: raw
  endian: le
seq:
  - id: header
    type: header
  - id: stages
    type: stage
    repeat: expr
    repeat-expr: header.stage_count
types:
  header:
    seq:
    - id: name
      type: str
      size: 16
      terminator: 0
      encoding: ASCII
    - id: timestamp
      type: u8
    - id: score
      type: u4
    - id: unknown_1
      size: 100
    - id: slowdown
      type: f4
    - id: stage_count
      type: u4
    - id: shot
      type: u4
    - id: subshot
      type: u4
    - id: difficulty
      type: u4
    - id: cleared
      type: u4
    - id: unknown_2
      type: u4
    - id: spell_practice_id
      type: u4
  stage:
    seq:
    - id: stage_num
      type: u2
    - id: rng
      type: u2
    - id: frame_count
      type: u4
    - id: end_off
      type: u4
    - id: pos_subpixel_x
      type: u4
    - id: pos_subpixel_y
      type: u4
    - id: stage_num_2
      type: u4
    - id: stage_num_3
      type: u4
    - id: chapter
      type: u4
    - id: time_in_stage
      type: u4
      repeat: expr
      repeat-expr: 3
    - id: shot
      type: u4
    - id: subshot
      type: u4
    - id: score
      type: u4
    - id: difficulty
      type: u4
    - id: continues
      type: u4
    - id: rank_unused
      type: u4
    - id: graze
      type: u4
    - id: unknown_1
      type: u4
    - id: spell_practice_id
      type: u4
    - id: miss_count
      type: u4
    - id: unknown_2
      type: u4
    - id: point_items_collected
      type: u4
    - id: piv
      type: u4
    - id: piv_min
      type: u4
    - id: piv_max
      type: u4
    - id: power
      type: u4
    - id: power_max
      type: u4
    - id: power_levelup
      type: u4
    - id: unknown_3
      type: u4
    - id: lives
      type: u4
    - id: life_pieces
      type: u4
    - id: unknown_4
      type: u4
    - id: bombs
      type: u4
    - id: bomb_pieces
      type: u4
    - id: bomb_restock_on_death
      type: u4
    - id: unknown_5
      type: u4
    - id: unknown_6
      type: u4
    - id: hyper_fill
      type: u4
    - id: tokens
      type: u4
      repeat: expr
      repeat-expr: 5
    - id: unknown_7
      type: u4
      repeat: expr
      repeat-expr: 6
    - id: unknown_timer
      type: timer
    - id: hyper_time
      type: timer
    - id: unknown_8
      type: u4
      repeat: expr
      repeat-expr: 3
    - id: hyper_flags
      type: u4
    - id: player_is_focused
      type: u4
    - id: spellcard_real_times
      type: u4
      repeat: expr
      repeat-expr: 21
    - id: stage_data
      size: end_off
  timer:
    seq:
    - id: prev_time
      type: u4
    - id: time
      type: u4
    - id: time_f
      type: f4
    - id: game_speed_ununsed
      type: u4
    - id: control
      type: u4