meta:
  id: th07
  file-extension: raw
  endian: le
seq:
  - id: file_header
    type: file_header
  - id: header
    type: header
types:
  file_header:
    seq:
      - id: magic
        contents: T7RP
      - id: version
        size: 2
      - id: unknown_1
        size: 7
      - id: key
        type: u1
      - id: unknown_2
        type: u2
      - id: unknown_3
        type: u4
      - id: comp_size
        type: u4
      - id: size
        type: u4
      - id: stage_offsets
        type: stage_pointer
        repeat: expr
        repeat-expr: 7
      - id: unknown_4
        type: u4
        repeat: expr
        repeat-expr: 7
  header:
    seq:
      - id: unknown_1
        size: 2
      - id: shot
        type: u1
      - id: difficulty
        type: u1
      - id: date
        type: str
        size: 6
        encoding: ASCII
        terminator: 0x0
      - id: name
        type: str
        encoding: SJIS
        terminator: 0x0
        size: 9
      - id: unknown_2
        size: 5
      - id: score
        type: u4
      - id: unknown_3
        type: u4
        repeat: expr
        repeat-expr: 23
      - id: slowdown
        type: f4
  stage_pointer:
    seq:
      - id: offset
        doc: Location of the stage struct
        type: u4
    instances:
      body:
        pos: offset
        type: stage
        if: offset != 0
  stage:
    seq:
      - id: score
        type: u4
      - id: point_items
        type: u4
      - id: piv
        type: u4
      - id: cherrymax
        type: u4
      - id: cherry
        type: u4
      - id: graze
        type: u4
      - id: unknown_1
        type: u4
      - id: unknown_2
        type: u4
      - id: unknown_3
        type: u2
      - id: power
        type: u1
      - id: lives
        type: u1
      - id: bombs
        type: u1
      - id: unknown_4
        type: u1