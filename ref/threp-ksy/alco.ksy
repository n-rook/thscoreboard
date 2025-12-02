meta:
  id: alco
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
        encoding: SJIS
      - id: timestamp
        type: u4
      - id: score
        type: u4
      - id: unknown_1
        size: 52
      - id: slowdown
        type: f4
      - id: stagecount
        type: u4
      - id: unknown_2
        size: 16
  stage:
    seq:
      - id: stage_num
        type: u2
      - id: unknown_1
        size: 6
      - id: len_stage_data
        type: u4
      - id: score
        type: u4
      - id: unknown_2
        size: 8
      - id: stage_data
        size: len_stage_data
