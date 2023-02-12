meta:
  id: th08_userdata
  file-extension: rpy
  endian: le
seq:
  - id: magic
    contents: T8RP
  - id: version
    size: 2
  - id: unknown
    size: 6
  - id: userdata_offset
    type: u4
instances:
  userdata:
    pos: userdata_offset
    type: userdata
types:
  userdata:
    seq:
      - id: magic_user
        contents: USER
      - id: user_length
        type: u4
      - id: unknown
        size: 4
      - id: name
        type: userdata_field
      - id: date
        type: userdata_field
      - id: shot
        type: userdata_field
      - id: score
        type: userdata_field
      - id: difficulty
        type: userdata_field
      - id: cleared
        type: userdata_field
      - id: mistakes
        type: userdata_field
      - id: bombs
        type: userdata_field
      - id: slowdown
        type: userdata_field
  crlfstring:
    seq:
      - id: value
        type: str
        terminator: 0xd
        encoding: SJIS
      - id: term
        type: u1
  userdata_field:
    seq:
      - id: name
        type: str
        terminator: 0x09
        encoding: ASCII
      - id: value
        type: str
        terminator: 0xd
        encoding: ASCII
      - id: term
        type: u1