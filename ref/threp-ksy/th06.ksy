meta:
  id: th06
  file-extension: rpy
  endian: le
seq:
  - id: file_header
    type: file_header
types:
  file_header:
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
        encoding: SJIS
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
        type: stage_pointer
        repeat: expr
        repeat-expr: 7
  stage_pointer:
    seq:
      - id: raw_offset
        doc: Raw offset, relative to encrypted file
        type: u4
    instances:
      offset:
        doc: Offset relative to decrypted file
        value: raw_offset - 15
      # See https://github.com/kaitai-io/kaitai_struct/issues/14
      # for an explanation of this pattern.
      body:
        pos: offset
        type: stage
        if: raw_offset != 0

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
