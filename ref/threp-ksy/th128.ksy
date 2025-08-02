meta:
  id: th128
  file-extension: raw
  endian: le
seq:
  - id: header
    type: header
  - id: stages
    type: stage
    repeat: expr
    repeat-expr: header.stagecount
types:
  header:
    seq:
      - id: name
        type: str
        size: 12
        terminator: 0x0
        encoding: SJIS
      - id: timestamp
        type: u8
      - id: score
        type: u4
      - id: unknown_1
        size: 60
      - id: slowdown
        type: f4
      - id: stagecount
        type: u4
      - id: route
        type: u4
      # ZUN never changes his replay formats...
      - id: subshot_unused
        type: u4
      # If this is 4, then route must be 6
      - id: difficulty
        type: u4
      # Also encodes the route, but encodes the clear status in addition to that
      - id: cleared
        type: u4
      - id: unknown_2
        size: 4
  stage:
    seq:
      - id: stage
        type: u2
      - id: seed
        type: u2
      - id: frames
        type: u4
      - id: len_stage_data
        type: u4
      - id: score
        type: u4
      - id: unknown_0
        type: u4
      - id: piv
        type: u4
      - id: unknown_1
        size: 8
      - id: continues
        type: u4
      - id: unknown_2
        size: 4
      - id: graze
        type: u4
      - id: unknown_3
        size: 84
      - id: motivation
        type: u4
      - id: perfect_freeze
        type: u4
      - id: frozen_area
        type: f4
      - id: unused_1
        size: 4
      - id: stage_data
        size: len_stage_data
