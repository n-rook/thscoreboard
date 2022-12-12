meta:
  id: th09
  file-extension: rpy
  endian: le
seq:
  - id: file_header
    type: file_header
  - id: header
    type: header
instances:
  stages:
    pos: file_header.stage_offsets[_index]
    type:
      switch-on: file_header.stage_offsets[_index]
      cases:
        0: dummy
        _: stage
    repeat: expr
    repeat-expr: 40
types:
  dummy:
    doc: blank type
  file_header:
    seq:
      - id: padding
        size: 32
      - id: stage_offsets
        type: u4
        repeat: expr
        repeat-expr: 40
  header:
    seq:
      - id: unknown_1
        type: u4
      - id: date
        type: str
        size: 10
        encoding: ASCII
        terminator: 0x0
      - id: name
        type: str
        size: 9
        encoding: ASCII
        terminator: 0x0
      - id: difficulty
        type: u1
  stage:
    seq:
      - id: score
        type: u4
      - id: pair
        type: u2
      - id: shot
        type: u1
      - id: ai
        type: b1
      - id: lives
        type: u1
      - id: unknown
        type: u1