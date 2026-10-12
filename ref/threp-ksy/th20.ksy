meta:
  id: th20
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
      encoding: Shift_JIS
    - id: timestamp
      type: u8
    - id: score
      type: u4
    - id: unknown_1
      size: 180
    - id: slowdown
      type: f4
    - id: stage_count
      type: u4
    - id: shot  # 0 is Reimu, 1 is Marisa
      type: u4
    # 0 red, 1 red2, 2 blue, 3 blue2, 4 yellow, 5 yellow2, 6 green, 7 green2, 8 default (sub only)
    # note that the first stone is the "main" stone
    - id: stones
      type: u4
      repeat: expr
      repeat-expr: 4
    - id: unknown_2
      size: 4
    - id: difficulty
      type: u4
    # Win on stage 3, this is 3. Die on stage 1, this is 1.
    # So probably related to stage_count or stage practice
    - id: unknown_3
      size: 4
    - id: unknown_4
      size: 4
    - id: spell_practice_id
      type: u4
  stage:
    seq:
    - id: stage_num
      type: u4
    - id: rng
      type: u4
    - id: frame_count
      type: u4
    - id: len_stage_data
      type: u4
    - id: pos_subpixel_x
      type: u4
    - id: pos_subpixel_y
      type: u4
    - id: unknown_1
      size: 88
    - id: score
      type: u4
    - id: unknown_2
      size: 44
    - id: power
      type: u4
    - id: power_max
      type: u4
    - id: unknown_3
      size: 4
    # Presumed graze, but in th20 it has no in-game meaning.
    - id: graze
      type: u4
    - id: unknown_4
      type: u4
    # Anomaly value, scaled by 5000.
    - id: piv
      type: u4
    - id: unknown_5
      type: u4
    - id: anomaly_attack_gauge
      type: u4
    - id: unknown_6
      size: 20
    # Presumed anomaly enemy gauges, ordered red, blue, yellow, green.
    - id: unknown_7
      size: 16
    # ordered red, blue, yellow, green.
    - id: stones_levels
      type: u4
      repeat: expr
      repeat-expr: 4
    #  ordered red, blue, yellow, green.
    - id: anomaly_levels
      type: u4
      repeat: expr
      repeat-expr: 4
    - id: total_stone_level
      type: u4
    - id: unknown_8
      size: 32
    - id: lives
      type: u4
    - id: lives_max
      type: u4
    - id: life_pieces
      type: u4
    - id: unknown_9
      size: 4
    - id: unknown_10
      size: 4
    - id: bombs
      type: u4
    - id: bomb_pieces
      type: u4
    - id: unknown_11
      size: 4
    - id: bombs_max
      type: u4
    - id: unknown_12
      size: 332
    - id: unknown_13
      type: f4
    - id: unknown_14
      type: f4
    - id: stage_data
      size: len_stage_data

# `anomaly_enemy_gauge` is not included in this KSY.
# Replay files store initial values at each stage for mid-game playback,
# while this service displays them as end-of-stage values. Since this gauge
# is transformed between stages, it cannot be compared in the same context.
