#include <gtest/gtest.h>
#include "util.hpp"
#include "ExtSized.pp.hpp"




TEST(generated_raw_arrays, BuiltinExtSized_1)
{
    test_swap<ExtSizedArrayA>(
        "\x01\x00"
        "\x02\x01\x00\x00\x00\x00"
        "\x05\x00\x05\x00\x05\x00\x05\x00",

        "\x01\x00"
        "\x01\x02\x00\x00\x00\x00"
        "\x00\x05\x00\x05\x00\x05\x00\x05"
    );
}

TEST(generated_raw_arrays, BuiltinExtSized_2)
{
    test_swap<ExtSizedArrayA>(
        "\x02\x00"
        "\x02\x01\x04\x03\x00\x00"
        "\x05\x00\x05\x00\x05\x00\x05\x00"
        "\x06\x00\x06\x00\x06\x00\x06\x00",

        "\x02\x00"
        "\x01\x02\x03\x04\x00\x00"
        "\x00\x05\x00\x05\x00\x05\x00\x05"
        "\x00\x06\x00\x06\x00\x06\x00\x06"
    );
}

TEST(generated_raw_arrays, BuiltinExtSized_3)
{
    test_swap<ExtSizedArrayA>(
        "\x03\x00"
        "\x02\x01\x04\x03\x06\x05"
        "\x06\x00\x06\x00\x06\x00\x06\x00"
        "\x07\x00\x07\x00\x07\x00\x07\x00"
        "\x08\x00\x08\x00\x08\x00\x08\x00",

        "\x03\x00"
        "\x01\x02\x03\x04\x05\x06"
        "\x00\x06\x00\x06\x00\x06\x00\x06"
        "\x00\x07\x00\x07\x00\x07\x00\x07"
        "\x00\x08\x00\x08\x00\x08\x00\x08"
    );
}

TEST(generated_raw_arrays, BuiltinExtSized_4)
{
    test_swap<BuiltinExtSizedB>(
        "\x00\x00\x00\x02"
        "\xDE\xAD\xBE\xEF"
        "\x01\x02"
        "\x04\x03\x06\x05\x00\x00"
        "\x0A\x09\x08\x07\x0E\x0D\x0C\x0B",

        "\x02\x00\x00\x00"
        "\xEF\xBE\xAD\xDE"
        "\x01\x02"
        "\x03\x04\x05\x06\x00\x00"
        "\x07\x08\x09\x0A\x0B\x0C\x0D\x0E"
    );
}

TEST(generated_raw_arrays, BuiltinExtSized_5)
{
    test_swap<DynFieldsExtSized>(
        "\x00\x00\x00\x02"
        "\x02\x00"
        "\x02\x01\x04\x03"
        "\x06\x05\x08\x07\x00\x00"
        "\x03\x00"
        "\x02\x01\x04\x03\x06\x05"
        "\x08\x07\x0A\x09\x0C\x0B\x00\x00",

        "\x02\x00\x00\x00"
        "\x02\x00"
        "\x01\x02\x03\x04"
        "\x05\x06\x07\x08\x00\x00"
        "\x03\x00"
        "\x01\x02\x03\x04\x05\x06"
        "\x07\x08\x09\x0A\x0B\x0C\x00\x00"
    );
}

