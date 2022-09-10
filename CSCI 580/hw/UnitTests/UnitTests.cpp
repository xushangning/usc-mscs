#include <format>
#include <array>
#include <type_traits>

#include "CppUnitTest.h"

#include "../2/rend.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

bool operator==(const GzPixel& x, const GzPixel& y) noexcept
{
    return x.red == y.red && x.green == y.green && x.blue == y.blue
        && x.alpha == y.alpha && x.z == y.z;
}

namespace Microsoft { namespace VisualStudio { namespace CppUnitTestFramework {
    template <>
    std::wstring ToString(const GzPixel& p) {
        return std::format(L"{{{}, {}, {}}}", p.red, p.green, p.blue);
    }
}}}

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
        
        TEST_METHOD(TestEmptyTriangles)
        {
            constexpr int TEST_REGION = 6;
            GzPixel background[TEST_REGION][TEST_REGION];
            for (int i = 0; i < TEST_REGION; ++i)
                for (int j = 0; j < TEST_REGION; ++j) {
                    auto& pixel = background[i][j];
                    render_.GzGet(i, j, &pixel.red, &pixel.green, &pixel.blue, &pixel.alpha, &pixel.z);
                }

            std::array argument_types = { GZ_POSITION, GZ_POSITION };
            Triangle triangles[]{
                // a small triangle that doesn't touch any pixel
                { {0.25, 0.25}, {5, 0.5}, {2.75, 1} },
                // a triangle degenerated into a segment
                { {0, 0, 0}, {3, 3, 3}, {5, 5, 5} },
            };
            GzPointer arguments[]{ triangles[0], triangles[1] };
            render_.GzPutTriangle(static_cast<int>(argument_types.size()), argument_types.data(), arguments);

            for (int i = 0; i < TEST_REGION; ++i)
                for (int j = 0; j < TEST_REGION; ++j) {
                    GzPixel pixel;
                    render_.GzGet(i, j, &pixel.red, &pixel.green, &pixel.blue, &pixel.alpha, &pixel.z);
                    Assert::AreEqual(background[i][j], pixel);
                }
        }
    };

    constexpr std::remove_extent_t<GzColor> kGzColorMax = 1;
    const GzColor UnitTests::kColor{ kGzColorMax, kGzColorMax, kGzColorMax };
}
