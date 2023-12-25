meta:
  id: th09
  file-extension: rpy
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
        contents: T9RP
      - id: version
        type: u2
      - id: unknown_1
        size: 6
      - id: comp_size
        type: u4
      - id: unknown_2
        type: u4
      - id: key
        type: u1
      - id: unknown_3
        size: 7
      - id: decomp_size
        type: u4
      - id: stage_offsets
        type: stage_pointer
        repeat: expr
        repeat-expr: 20
      - id: unknown_offsets
        type: u4
        repeat: expr
        repeat-expr: 20
        doc: These look like more stage offsets, but I have no idea what they do or what they're for, and they're causing EOF errors when trying to parse them as stages sometimes, so I've chosen to ignore them
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
        encoding: SJIS
        terminator: 0x0
      - id: difficulty
        type: u1
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