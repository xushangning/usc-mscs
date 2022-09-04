#include <type_traits>

#include "CppUnitTest.h"

#include "../2/rend.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
    TEST_CLASS(UnitTests)
    {
        GzRender render_{ 128, 128 };

        static const GzColor kColor;

    public:

        UnitTests()
        {
            auto argument_type = GZ_RGB_COLOR;
            void* argument = const_cast<GzColor*>(&kColor);
            render_.GzPutAttribute(1, &argument_type, &argument);
        }

        TEST_METHOD_INITIALIZE(InitializeMethod)
        {
            render_.GzDefault();
        }
    };

    constexpr std::remove_extent_t<GzColor> kGzColorMax = 1;
    const GzColor UnitTests::kColor{ kGzColorMax, kGzColorMax, kGzColorMax };
}
