meta:
  id: th07_comp
  file-extension: rpy
  endian: le
seq:
  - id: header
    type: header
types:
  dummy:
    doc: blank type
  header:
    seq:
      - id: unknown_3
        type: u4
      - id: comp_size
        type: u4
      - id: size
        type: u4