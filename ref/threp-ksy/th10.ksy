meta:
  id: th10
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
      - id: shot
        type: u4
      - id: subshot
        type: u4
      - id: difficulty
        type: u4
      - id: unknown_3
        type: u4
      - id: unknown_4
        type: u4
  stage:
    seq:
      - id: stage_num
        type: u2
      - id: unknown_1
        type: u2
      - id: unknown_2
        type: u4
      - id: next_stage_offset
        type: u4
        doc: add to current stage offset, + current stage header length which is 0x1c4
      - id: score
        type: u4
      - id: power
        type: u4
      - id: piv
        type: u4
      - id: unknown_3
        type: u4
      - id: lives
        type: u4
      - id: rest_of_header
        size: 420
      - id: stage_data
        size: next_stage_offset
