meta:
  id: th06
  file-extension: rpy
  endian: le
seq:
  - id: header
    type: header
instances:
  stages:
    pos: header.stage_offsets[_index]
    type:
      switch-on: header.stage_offsets[_index]
      cases:
        0: dummy
        _: stage
    repeat: expr
    repeat-expr: 7
types:
  dummy:
    doc: blank type
  header:
    seq:
      - id: unknown_2
        type: u1
      - id: date
        type: str
        size: 9
        encoding: ASCII
        terminator: 0x0
      - id: name
        type: str
        size: 9
        encoding: ASCII
        terminator: 0x0
      - id: unknown_3
        type: u2
      - id: score
        type: u4
      - id: unknown_4
        type: u4
      - id: slowdown
        type: f4
      - id: unknown_5
        type: u4
      - id: stage_offsets
        type: u4
        repeat: expr
        repeat-expr: 7
  stage:
    seq:
      - id: score
        type: u4
      - id: seed
        type: u2
      - id: unknown_1
        type: u2
      - id: power
        type: u1
      - id: lives
        type: s1
      - id: bombs
        type: s1
      - id: rank
        type: u1
