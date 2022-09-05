#include <type_traits>

#include "CppUnitTest.h"

#include "../2/rend.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
    TEST_CLASS(UnitTests)
    {
        GzRender render_{ 128, 128 };

        typedef GzCoord Triangle[3];

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

        TEST_METHOD(TestZIndexInterpolation)
        {
            constexpr int C = 4;
            // a triangle formed by the intersection of the surface
            // x + y + z = C and the first octant
            Triangle triangle{ {C, 0, 0}, {0, C, 0}, {0, 0, C} };
            auto argument_type = GZ_POSITION;
            void* argument = &triangle;
            render_.GzPutTriangle(1, &argument_type, &argument);

            // x and y start at 1 to avoid the triangle's sides.
            for (int x = 1; x < C; ++x)
                for (int y = 1; y < C - x; ++y) {
                    GzPixel pixel;
                    render_.GzGet(x, y, &pixel.red, &pixel.green, &pixel.blue, &pixel.alpha, &pixel.z);

                    Assert::AreEqual(render_.ctoi(kColor[0]), pixel.red);
                    Assert::AreEqual(render_.ctoi(kColor[1]), pixel.green);
                    Assert::AreEqual(render_.ctoi(kColor[2]), pixel.blue);
                    Assert::AreEqual(C - x - y, pixel.z);
                }
        }
    };

    constexpr std::remove_extent_t<GzColor> kGzColorMax = 1;
    const GzColor UnitTests::kColor{ kGzColorMax, kGzColorMax, kGzColorMax };
}
