import pytest
from prophyc import model
from prophyc.generators.cpp_full import (
    generate_struct_encode,
    generate_union_encode
)

def process(nodes):
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes)
    return nodes

@pytest.fixture
def Builtin():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('BuiltinFixed', [
            model.StructMember('x', 'u32', size = 2)
        ]),
        model.Struct('BuiltinDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('BuiltinLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('BuiltinGreedy', [
            model.StructMember('x', 'u32', unlimited = True)
        ])
    ])

@pytest.fixture
def Fixcomp():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('Fixcomp', [
            model.StructMember('x', 'Builtin'),
            model.StructMember('y', 'Builtin')
        ]),
        model.Struct('FixcompFixed', [
            model.StructMember('x', 'Builtin', size = 2)
        ]),
        model.Struct('FixcompDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Builtin', bound = 'num_of_x')
        ]),
        model.Struct('FixcompLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Builtin', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('FixcompGreedy', [
            model.StructMember('x', 'Builtin', unlimited = True)
        ])
    ])

@pytest.fixture
def Unions():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Union('Union', [
            model.UnionMember('a', 'u8', '1'),
            model.UnionMember('b', 'u32', '2'),
            model.UnionMember('c', 'Builtin', '3')
        ]),
        model.Struct('BuiltinOptional', [
            model.StructMember('x', 'u32', optional = True)
        ]),
        model.Struct('FixcompOptional', [
            model.StructMember('x', 'Builtin', optional = True)
        ])
    ])

@pytest.fixture
def Enums():
    return process([
        model.Enum('Enum', [
            model.EnumMember('Enum_One', '1'),
            model.EnumMember('Enum_Two', '2')
        ]),
        model.Struct('DynEnum', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Enum', bound = 'num_of_x')
        ])
    ])

@pytest.fixture
def Floats():
    return process([
        model.Struct('Floats', [
            model.StructMember('a', 'r32'),
            model.StructMember('b', 'r64')
        ])
    ])

@pytest.fixture
def Bytes():
    return process([
        model.Struct('BytesFixed', [
            model.StructMember('x', 'byte', size = 3)
        ]),
        model.Struct('BytesDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'byte', bound = 'num_of_x')
        ]),
        model.Struct('BytesLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'byte', size = 4, bound = 'num_of_x')
        ]),
        model.Struct('BytesGreedy', [
            model.StructMember('x', 'byte', unlimited = True)
        ])
    ])

@pytest.fixture
def Dyncomp():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('Dyncomp', [
            model.StructMember('x', 'Builtin'),
            model.StructMember('y', 'Builtin')
        ]),
        model.Struct('DyncompDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Builtin', bound = 'num_of_x')
        ]),
        model.Struct('DyncompGreedy', [
            model.StructMember('x', 'Builtin', unlimited = True)
        ])
    ])

@pytest.fixture
def Endpad():
    return process([
        model.Struct('Endpad', [
            model.StructMember('x', 'u16'),
            model.StructMember('y', 'u8')
        ]),
        model.Struct('EndpadFixed', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', size = 3)
        ]),
        model.Struct('EndpadDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x')
        ]),
        model.Struct('EndpadLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('EndpadGreedy', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', unlimited = True)
        ])
    ])

@pytest.fixture
def Scalarpad():
    return process([
        model.Struct('Scalarpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'u16')
        ]),
        model.Struct('ScalarpadComppre_Helper', [
            model.StructMember('x', 'u8')
        ]),
        model.Struct('ScalarpadComppre', [
            model.StructMember('x', 'ScalarpadComppre_Helper'),
            model.StructMember('y', 'u16')
        ]),
        model.Struct('ScalarpadComppost_Helper', [
            model.StructMember('x', 'u16')
        ]),
        model.Struct('ScalarpadComppost', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'ScalarpadComppost_Helper')
        ]),
    ])

@pytest.fixture
def Unionpad():
    return process([
        model.Struct('UnionpadOptionalboolpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'u8', optional = True)
        ]),
        model.Struct('UnionpadOptionalvaluepad', [
            model.StructMember('x', 'u64', optional = True)
        ]),
        model.Union('UnionpadDiscpad_Helper', [
            model.UnionMember('a', 'u8', '1')
        ]),
        model.Struct('UnionpadDiscpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'UnionpadDiscpad_Helper')
        ]),
        model.Union('UnionpadArmpad_Helper', [
            model.UnionMember('a', 'u8', '1'),
            model.UnionMember('b', 'u64', '2')
        ]),
        model.Struct('UnionpadArmpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'UnionpadArmpad_Helper')
        ])
    ])

@pytest.fixture
def Arraypad():
    return process([
        model.Struct('ArraypadCounter', [
            model.StructMember('num_of_x', 'u8'),
            model.StructMember('x', 'u16', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterSeparated', [
            model.StructMember('num_of_x', 'u8'),
            model.StructMember('y', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterAligns_Helper', [
            model.StructMember('num_of_x', 'u16'),
            model.StructMember('x', 'u8', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterAligns', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'ArraypadCounterAligns_Helper')
        ]),
        model.Struct('ArraypadFixed', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', size = 3),
            model.StructMember('z', 'u32')
        ]),
        model.Struct('ArraypadDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('ArraypadLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', size = 2, bound = 'num_of_x'),
            model.StructMember('y', 'u32')
        ])
    ])

def test_generate_builtin_encode(Builtin):
    assert generate_struct_encode(Builtin[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Builtin[1]) == """\
pos = do_encode<E>(pos, x.x, 2);
"""
    assert generate_struct_encode(Builtin[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Builtin[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 8;
"""
    assert generate_struct_encode(Builtin[4]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_fixcomp_encode(Fixcomp):
    assert generate_struct_encode(Fixcomp[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Fixcomp[2]) == """\
pos = do_encode<E>(pos, x.x, 2);
"""
    assert generate_struct_encode(Fixcomp[3]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Fixcomp[4]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 16;
"""
    assert generate_struct_encode(Fixcomp[5]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_dyncomp_encode(Dyncomp):
    assert generate_struct_encode(Dyncomp[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Dyncomp[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Dyncomp[3]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_unions_encode(Unions):
    assert generate_union_encode(Unions[1]) == """\
pos = do_encode<E>(pos, x.discriminator);
switch(x.discriminator)
{
    case Union::discriminator_a: do_encode<E>(pos, x.a); break;
    case Union::discriminator_b: do_encode<E>(pos, x.b); break;
    case Union::discriminator_c: do_encode<E>(pos, x.c); break;
}
pos = pos + 8;
"""
    assert generate_struct_encode(Unions[2]) == """\
pos = do_encode<E>(pos, x.has_x);
if (x.has_x) do_encode<E>(pos, x.x);
pos = pos + 4;
"""
    assert generate_struct_encode(Unions[3]) == """\
pos = do_encode<E>(pos, x.has_x);
if (x.has_x) do_encode<E>(pos, x.x);
pos = pos + 8;
"""

def test_generate_enums_encode(Enums):
    assert generate_struct_encode(Enums[1]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""

def test_generate_floats_encode(Floats):
    assert generate_struct_encode(Floats[0]) == """\
pos = do_encode<E>(pos, x.a);
pos = pos + 4;
pos = do_encode<E>(pos, x.b);
"""

def test_generate_bytes_encode(Bytes):
    assert generate_struct_encode(Bytes[0]) == """\
pos = do_encode<E>(pos, x.x, 3);
"""
    assert generate_struct_encode(Bytes[1]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Bytes[2]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(4))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(4))));
pos = pos + 4;
"""
    assert generate_struct_encode(Bytes[3]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_endpad_encode(Endpad):
    assert generate_struct_encode(Endpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
pos = pos + 1;
"""
    assert generate_struct_encode(Endpad[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y, 3);
pos = pos + 1;
"""
    assert generate_struct_encode(Endpad[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Endpad[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 2;
pos = pos + 2;
"""
    assert generate_struct_encode(Endpad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y.data(), x.y.size());
pos = align<4>(pos);
"""

def test_generate_scalarpad_encode(Scalarpad):
    assert generate_struct_encode(Scalarpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Scalarpad[2]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Scalarpad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""

def test_generate_unionpad_encode(Unionpad):
    assert generate_struct_encode(Unionpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 3;
pos = do_encode<E>(pos, x.has_y);
if (x.has_y) do_encode<E>(pos, x.y);
pos = pos + 1;
pos = pos + 3;
"""
    assert generate_struct_encode(Unionpad[1]) == """\
pos = do_encode<E>(pos, x.has_x);
pos = pos + 4;
if (x.has_x) do_encode<E>(pos, x.x);
pos = pos + 8;
"""
    assert generate_union_encode(Unionpad[2]) == """\
pos = do_encode<E>(pos, x.discriminator);
switch(x.discriminator)
{
    case UnionpadDiscpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
}
pos = pos + 4;
"""
    assert generate_struct_encode(Unionpad[3]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 3;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_union_encode(Unionpad[4]) == """\
pos = do_encode<E>(pos, x.discriminator);
pos = pos + 4;
switch(x.discriminator)
{
    case UnionpadArmpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
    case UnionpadArmpad_Helper::discriminator_b: do_encode<E>(pos, x.b); break;
}
pos = pos + 8;
"""
    assert generate_struct_encode(Unionpad[5]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 7;
pos = do_encode<E>(pos, x.y);
"""

def test_generate_arraypad_encode(Arraypad):
    assert generate_struct_encode(Arraypad[0]) == """\
pos = do_encode<E>(pos, uint8_t(x.x.size()));
pos = pos + 1;
pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
"""
    assert generate_struct_encode(Arraypad[1]) == """\
pos = do_encode<E>(pos, uint8_t(x.x.size()));
pos = pos + 3;
pos = do_encode<E>(pos, x.y);
pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
"""
    assert generate_struct_encode(Arraypad[2]) == """\
pos = do_encode<E>(pos, uint16_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint16_t(x.x.size()));
pos = align<2>(pos);
"""
    assert generate_struct_encode(Arraypad[3]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Arraypad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y, 3);
pos = pos + 1;
pos = do_encode<E>(pos, x.z);
"""
    assert generate_struct_encode(Arraypad[5]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Arraypad[6]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 2;
pos = pos + 2;
pos = do_encode<E>(pos, x.y);
"""