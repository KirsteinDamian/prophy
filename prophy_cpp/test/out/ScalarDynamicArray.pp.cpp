#include "ScalarDynamicArray.pp.hpp"

namespace prophy
{

template <>
ScalarDynamicArray* swap<ScalarDynamicArray>(ScalarDynamicArray* payload)
{
    swap(&payload->num_of_x);
    return cast<ScalarDynamicArray*>(swap_n_fixed(payload->x, payload->num_of_x));
}

} // namespace prophy