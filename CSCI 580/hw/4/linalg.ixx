export module linalg;

import <valarray>;

import "gz.h";

using std::valarray;

export constexpr bool Is3x3Diagonal(const GzMatrix m) noexcept
{
	return !(m[0][1] || m[0][2] || m[1][0] || m[1][2] || m[2][0] || m[2][1]);
}

export bool MatValarrayMul(const GzMatrix lhs, valarray<float>& rhs)
{
	float temp[4];
	for (int i = 0; i < 4; ++i)
		temp[i] = lhs[i][0] * rhs[0] + lhs[i][1] * rhs[1] + lhs[i][2] * rhs[2] + lhs[i][3];

	if (temp[3] == 0.0f)
		return false;
	for (int i = 0; i < 3; ++i)
		rhs[i] = temp[i] / temp[3];
	return true;
}

export inline float Dot(const valarray<float>& lhs, const valarray<float>& rhs)
{
	return (lhs * rhs).sum();
}
