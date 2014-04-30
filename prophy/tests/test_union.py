import prophy
import pytest

def make_U():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u32, 1),
                       ("c", prophy.u32, 2)]
    return U()

def test_simple_union():
    x = make_U()

    assert 0 == x.discriminator
    assert 0 == x.a
    assert 'a: 0\n' == str(x)
    assert '\x00\x00\x00\x00\x00\x00\x00\x00' == x.encode(">")

    x.decode('\x02\x00\x00\x00\x10\x00\x00\x00', "<")

    assert 2 == x.discriminator
    assert 16 == x.c
    assert 'c: 16\n' == str(x)
    assert '\x00\x00\x00\x02\x00\x00\x00\x10' == x.encode(">")

def test_simple_union_discriminator_accepts_ints_or_field_name_and_clears():
    x = make_U()

    x.a = 42
    x.discriminator = 1

    assert 0 == x.b
    assert 'b: 0\n' == str(x)
    assert '\x00\x00\x00\x01\x00\x00\x00\x00' == x.encode(">")

    x.discriminator = "c"

    assert 0 == x.c
    assert 'c: 0\n' == str(x)
    assert '\x00\x00\x00\x02\x00\x00\x00\x00' == x.encode(">")

def test_union_copy_from():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u32, 1)]

    x = U()
    x.discriminator = "b"
    x.b = 3

    y = U()
    assert 0 == y.discriminator
    assert 0 == y.a

    y.copy_from(x)
    assert 1 == y.discriminator
    assert 3 == y.b

def test_simple_union_discriminator_does_not_clear_fields_if_set_to_same_value():
    x = make_U()

    x.a = 42

    x.discriminator = 0

    assert 42 == x.a

    x.discriminator = "a"

    assert 42 == x.a

def test_union_nonsequential_discriminators():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 3),
                       ("b", prophy.u32, 10),
                       ("c", prophy.u32, 55)]
    x = U()
    assert 3 == x.discriminator

    x.discriminator = 3
    assert 3 == x.discriminator
    assert 0 == x.a

    x.discriminator = 10
    assert 10 == x.discriminator
    assert 0 == x.b

    x.discriminator = 55
    assert 55 == x.discriminator
    assert 0 == x.c

    x.discriminator = "a"
    assert 3 == x.discriminator
    assert 0 == x.a

    x.discriminator = "b"
    assert 10 == x.discriminator
    assert 0 == x.b

    x.discriminator = "c"
    assert 55 == x.discriminator
    assert 0 == x.c

def make_UVarLen():
    class UVarLen(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2),
                       ("d", prophy.u64, 3)]
    return UVarLen()

def test_union_size():
    assert 8 == make_U()._SIZE
    assert 12 == make_UVarLen()._SIZE

def test_union_encode_according_to_largest_field():
    x = make_UVarLen()

    x.discriminator = "a"
    x.a = 0x12
    assert "\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert "\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "b"
    x.b = 0x1234
    assert "\x00\x00\x00\x01\x12\x34\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert "\x01\x00\x00\x00\x34\x12\x00\x00\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "c"
    x.c = 0x12345678
    assert "\x00\x00\x00\x02\x12\x34\x56\x78\x00\x00\x00\x00" == x.encode(">")
    assert "\x02\x00\x00\x00\x78\x56\x34\x12\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "d"
    x.d = 0x123456789ABCDEF1
    assert "\x00\x00\x00\x03\x12\x34\x56\x78\x9a\xbc\xde\xf1" == x.encode(">")
    assert "\x03\x00\x00\x00\xf1\xde\xbc\x9a\x78\x56\x34\x12" == x.encode("<")

def test_union_decode_according_to_largest_field():
    x = make_UVarLen()

    assert 12 == x.decode("\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00", ">")
    assert 0 == x.discriminator
    assert 0x12 == x.a

    assert 12 == x.decode("\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00", "<")
    assert 0 == x.discriminator
    assert 0x12 == x.a

    assert 12 == x.decode("\x00\x00\x00\x01\x12\x34\x00\x00\x00\x00\x00\x00", ">")
    assert 1 == x.discriminator
    assert 0x1234 == x.b

    assert 12 == x.decode("\x01\x00\x00\x00\x34\x12\x00\x00\x00\x00\x00\x00", "<")
    assert 1 == x.discriminator
    assert 0x1234 == x.b

    assert 12 == x.decode("\x00\x00\x00\x02\x12\x34\x56\x78\x00\x00\x00\x00", ">")
    assert 2 == x.discriminator
    assert 0x12345678 == x.c

    assert 12 == x.decode("\x02\x00\x00\x00\x78\x56\x34\x12\x00\x00\x00\x00", "<")
    assert 2 == x.discriminator
    assert 0x12345678 == x.c

    assert 12 == x.decode("\x00\x00\x00\x03\x12\x34\x56\x78\x9a\xbc\xde\xf1", ">")
    assert 3 == x.discriminator
    assert 0x123456789ABCDEF1 == x.d

    assert 12 == x.decode("\x03\x00\x00\x00\xf1\xde\xbc\x9a\x78\x56\x34\x12", "<")
    assert 3 == x.discriminator
    assert 0x123456789ABCDEF1 == x.d

def test_union_with_struct():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32),
                       ("b", prophy.u32)]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u16, 0),
                       ("b", S, 1)]

    x = U()
    assert x.encode(">") == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    x.a = 0x15
    assert x.encode(">") == "\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00"
    assert x.encode("<") == "\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00"

    x.discriminator = "b"
    assert x.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00"
    assert x.encode("<") == "\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    x.b.a = 0x15
    assert x.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x15\x00\x00\x00\x00"
    assert x.encode("<") == "\x01\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00"
    x.b.b = 0x20
    assert x.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x15\x00\x00\x00\x20"
    assert x.encode("<") == "\x01\x00\x00\x00\x15\x00\x00\x00\x20\x00\x00\x00"

    x.decode("\x00\x00\x00\x00\x25\x00\x00\x00\x00\x00\x00\x00", "<")
    assert x.discriminator == 0
    assert x.a == 0x25

    x.decode("\x00\x00\x00\x00\x00\x25\x00\x00\x00\x00\x00\x00", ">")
    assert x.discriminator == 0
    assert x.a == 0x25

    x.decode("\x01\x00\x00\x00\x25\x00\x00\x00\x35\x00\x00\x00", "<")
    assert x.discriminator == 1
    assert x.b.a == 0x25
    assert x.b.b == 0x35

    x.decode("\x00\x00\x00\x01\x00\x00\x00\x25\x00\x00\x00\x35", ">")
    assert x.discriminator == 1
    assert x.b.a == 0x25
    assert x.b.b == 0x35

def test_union_discriminator_exceptions():
    x = make_UVarLen()

    with pytest.raises(Exception) as e:
        x.b
    assert "currently field 0 is discriminated" == e.value.message

    x.discriminator = 1
    x.b = 42

    with pytest.raises(Exception) as e:
        x.a
    assert "currently field 1 is discriminated" == e.value.message

    with pytest.raises(Exception) as e:
        x.a = 1
    assert "currently field 1 is discriminated" == e.value.message

    with pytest.raises(Exception) as e:
        x.discriminator = "xxx"
    assert "unknown discriminator" == e.value.message

    with pytest.raises(Exception) as e:
        x.discriminator = 666
    assert "unknown discriminator" == e.value.message

    assert 1 == x.discriminator
    assert 42 == x.b

def test_union_decode_exceptions():
    x = make_UVarLen()

    with pytest.raises(Exception) as e:
        x.decode("\x00\x00\x00\xff", ">")
    assert "unknown discriminator" == e.value.message

    with pytest.raises(Exception) as e:
        x.decode("\x00\x00\x00\x02\x12\x34\x56\x78\x00\x00\x00\x00\x00", ">")
    assert "not all bytes read" == e.value.message

    with pytest.raises(Exception) as e:
        x.decode("\x00\x00\x00\x02\x12\x34\x56\x78\x00\x00\x00", ">")
    assert "not enough bytes" == e.value.message

def test_struct_with_union():
    class UVarLen(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u8, 1),
                       ("c", prophy.u8, 2)]
    class StructWithU(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", UVarLen),
                       ("c", prophy.u32)]

    x = StructWithU()

    x.a = 1
    x.b.discriminator = 2
    x.b.c = 3
    x.c = 4

    assert "\x01\x00\x00\x00\x02\x03\x00\x00\x00\x00\x00\x00\x04" == x.encode(">")
    assert "\x01\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00" == x.encode("<")

    x.decode("\x0a\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x20", ">")

    assert 10 == x.a
    assert 0 == x.b.discriminator
    assert 1024 == x.b.a
    assert 32 == x.c

    assert """\
a: 10
b {
  a: 1024
}
c: 32
""" == str(x)

def test_array_with_union():
    class UVarLen(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u16, 0),
                       ("b", prophy.u8, 1),
                       ("c", prophy.u8, 2)]
    class StructWithU(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(UVarLen, bound = "a_len"))]

    x = StructWithU()

    y = x.a.add()
    y.discriminator = "a"
    y.a = 1
    y = x.a.add()
    y.discriminator = "b"
    y.b = 2
    y = x.a.add()
    y.discriminator = "c"
    y.c = 3

    assert "\x03\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x02\x00\x00\x00\x00\x02\x03\x00" == x.encode(">")
    assert "\x03\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x02\x00\x02\x00\x00\x00\x03\x00" == x.encode("<")

    x.decode("\x02\x00\x00\x00\x01\x01\x00\x00\x00\x00\x02\x02\x00", ">")

    assert """\
a {
  b: 1
}
a {
  c: 2
}
""" == str(x)

def test_union_with_plain_struct():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u8)]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", S, 1)]

    x = U()
    x.discriminator = 1
    x.b.a = 2
    x.b.b = 3

    assert "\x00\x00\x00\x01\x02\x03" == x.encode(">")

    x.decode("\x00\x00\x00\x01\x06\x07", ">")
    assert 1 == x.discriminator
    assert 6 == x.b.a
    assert 7 == x.b.b

    assert """\
b {
  a: 6
  b: 7
}
""" == str(x)

def test_union_with_struct_with_array_and_bytes():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]
    class SBytesSized(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.bytes(size = 3))]
    class SArraySized(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.array(S, size = 3))]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", SBytesSized, 0),
                       ("b", SArraySized, 1)]

    x = U()
    x.discriminator = 0
    x.a.a = "abc"

    assert "\x00\x00\x00\x00abc" == x.encode(">")

    x.discriminator = 1
    x.b.a[0].a = 3
    x.b.a[1].a = 4
    x.b.a[2].a = 5
    assert "\x00\x00\x00\x01\x03\x04\x05" == x.encode(">")

    x.decode("\x00\x00\x00\x01\x07\x08\x09", ">")
    assert 1 == x.discriminator
    assert 7 == x.b.a[0].a
    assert 8 == x.b.a[1].a
    assert 9 == x.b.a[2].a

    assert """\
b {
  a {
    a: 7
  }
  a {
    a: 8
  }
  a {
    a: 9
  }
}
""" == str(x)

def test_union_with_nested_struct_and_union():
    class SInner(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", SInner)]
    class UInner(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1)]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", UInner, 0),
                       ("b", S, 1)]

    x = U()
    x.discriminator = 0
    x.a.discriminator = 1
    x.a.b = 0xFFF
    assert "\x00\x00\x00\x00\x00\x00\x00\x01\x0f\xff" == x.encode(">")

    x = U()
    x.discriminator = 1
    x.b.a.a = 0xF
    assert "\x00\x00\x00\x01\x0f\x00\x00\x00\x00\x00" == x.encode(">")

    x.decode("\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08", ">")
    assert 8 == x.a.b

    assert """\
a {
  b: 8
}
""" == str(x)

    y = U()
    y.copy_from(x)
    assert 0 == y.discriminator
    assert 1 == y.a.discriminator
    assert 8 == y.a.b

def test_union_with_typedef_and_enum():
    TU16 = prophy.u16
    class E(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", TU16, 0),
                       ("b", E, 1)]

    x = U()
    x.discriminator = "a"
    x.a = 17
    assert "\x00\x00\x00\x00\x00\x11\x00\x00" == x.encode(">")

    x.discriminator = "b"
    x.b = "E_2"
    assert "\x00\x00\x00\x01\x00\x00\x00\x02" == x.encode(">")

    x.decode("\x00\x00\x00\x01\x00\x00\x00\x01", ">")
    assert 1 == x.discriminator
    assert 1 == x.b

    assert """\
b: E_1
""" == str(x)

def test_union_exceptions_with_dynamic_arrays_and_bytes():
    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a", prophy.array(prophy.u32), 0)]
    assert "dynamic types not allowed in union" == e.value.message

    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.array(prophy.u32, bound = "a_len"), 1)]
    assert "dynamic types not allowed in union" == e.value.message

    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a", prophy.bytes(), 0)]
    assert "dynamic types not allowed in union" == e.value.message

    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.bytes(bound = "a_len"), 1)]
    assert "dynamic types not allowed in union" == e.value.message

def test_union_exceptions_with_nested_limited_greedy_dynamic_arrays_and_bytes():
    with pytest.raises(Exception) as e:
        class S2(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.array(prophy.u32))]
        class S(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", S2)]
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a", S, 0)]
    assert "dynamic types not allowed in union" == e.value.message

def test_union_with_limited_array_and_bytes():
    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.bytes(bound = "a_len", size = 3), 1)]
    assert "bound array/bytes not allowed in union" == e.value.message

    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.array(prophy.u32, bound = "a_len", size = 3), 1)]
    assert "bound array/bytes not allowed in union" == e.value.message

    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a", prophy.array(prophy.u8, size = 3), 0)]
    assert "static array not implemented in union" == e.value.message

def test_union_with_static_bytes():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.bytes(size = 3), 0)]

    x = U()

    assert "\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.decode("\x00\x00\x00\x00\x01\x02\x03", "<")

    assert """\
a: '\\x01\\x02\\x03'
""" == str(x)