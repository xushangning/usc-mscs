export module linalg;

import "gz.h";

export constexpr bool Is3x3Diagonal(const GzMatrix m) noexcept
{
	return !(m[0][1] || m[0][2] || m[1][0] || m[1][2] || m[2][0] || m[2][1]);
}
