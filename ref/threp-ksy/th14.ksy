meta:
  id: th14
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
      size: 12
      terminator: 0
      encoding: SJIS
    - id: timestamp
      type: u8
    - id: score
      type: u4
    - id: unknown_1
      size: 92
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
    - id: len_stage_data
      type: u4
    - id: pos_subpixel_x
      type: u4
    - id: pos_subpixel_y
      type: u4
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
    - id: unknown_1
      type: u4
    - id: graze
      type: u4
    - id: spell_practice_id
      type: u4
    - id: unknown_2
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
    - id: lives
      type: u4
    - id: life_pieces
      type: u4
    - id: unknown_3
      type: u4
    - id: bombs
      type: u4
    - id: bomb_pieces
      type: u4
    - id: score_from_poc
      type: u4
    - id: unknown_4
      type: u4
    - id: unknown_5
      type: u4
    - id: unknown_6
      type: u4
    - id: last_item_collected_pos
      type: f4
      repeat: expr
      repeat-expr: 3
    - id: poc_count
      type: u4
    - id: focused
      type: u4
    - id: spellcard_real_times
      type: u4
      repeat: expr
      repeat-expr: 21
    - id: stage_data
      size: len_stage_data
