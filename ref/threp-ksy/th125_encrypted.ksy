meta:
  id: th125_encrypted
  file-extension: rpy
  endian: le
seq:
  - id: header
    type: file_header
instances:
  userdata:
    pos: header.userdata_offset
    type: userdata
types:
  file_header:
    seq:
      - id: magic
        contents: t125
      # Probably includes version
      - id: unknown_1
        size: 8
      - id: userdata_offset
        type: u4
  userdata:
    seq:
      - id: magic_user
        contents: USER
      - id: user_length
        type: u4
      - id: unknown
        size: 4
      - id: user_desc
        type: u1
        repeat: until
        repeat-until: _ == 0xd
      - id: user_desc_term
        type: str
        terminator: 0xa
        encoding: ASCII
      - id: version
        type: userdata_field("Version")
      - id: username
        type: userdata_field("Name")
      - id: date
        type: userdata_field("Date")
      - id: shot
        type: userdata_field("Chara")
      - id: level_scene
        type: level_scene_field
      - id: score
        type: userdata_field("Score")
      - id: slowdown
        type: userdata_field("Slow Rate")
  userdata_field:
    params:
      - id: expected_name
        type: str
    seq:
      - id: name
        type: str
        size: expected_name.length
        encoding: ASCII
        valid: expected_name
      - id: name_value_separator_space
        contents: " "
      - id: value_with_space
        type: str
        # Always ends with 0x0d0a; that is, space then LF
        terminator: 0x0a
        encoding: ASCII
    instances:
      value:
        value: value_with_space.substring(0, value_with_space.length - 1)
  level_scene_field:
    seq:
      - id: level
        type: str
        terminator: 0x2d
        include: false
        encoding: ASCII
      - id: scene
        type: str
        include: false
        terminator: 0x0d
        encoding: ASCII
      - id: lf
        contents: [0x0a]
