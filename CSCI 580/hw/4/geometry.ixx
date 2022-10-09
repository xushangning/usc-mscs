export module geometry;

import <array>;
import <cmath>;

import "gz.h";

export class Vector
{
	std::array<float, 3> data_;

public:
	Vector(const GzCoord& data) noexcept : data_(std::to_array(data)) {}

	float& operator[](std::size_t index) noexcept { return data_[index]; }
	float operator[](std::size_t index) const noexcept { return data_[index]; }

	Vector operator-(const Vector& other) const noexcept
	{
		return GzCoord{data_[0] - other.data_[0], data_[1] - other.data_[1], data_[2] - other.data_[2]};
	}

	Vector& operator-=(const Vector& other) noexcept
	{
		data_[0] -= other.data_[0];
		data_[1] -= other.data_[1];
		data_[2] -= other.data_[2];
		return *this;
	}

	float Dot(const Vector& other) const noexcept
	{
		return data_[0] * other.data_[0] + data_[1] * other.data_[1] + data_[2] * other.data_[2];
	}

	Vector Cross(const Vector& other) const noexcept
	{
		return GzCoord{
			data_[1] * other.data_[2] - data_[2] * other.data_[1],
			data_[2] * other.data_[0] - data_[0] * other.data_[2],
			data_[0] * other.data_[1] - data_[1] * other.data_[0]
		};
	}

	Vector& operator/=(float c) noexcept
	{
		data_[0] /= c;
		data_[1] /= c;
		data_[2] /= c;
		return *this;
	}
};

export Vector operator*(float c, const Vector& v) noexcept
{
	return GzCoord{ v[0] * c, v[1] * c, v[2] * c };
}

export float abs(const Vector& v) noexcept
{
	return std::sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
}

export void MatMul(GzMatrix result, const GzMatrix lhs, const GzMatrix rhs)
{
	for (int i = 0; i < 4; ++i)
		for (int j = 0; j < 4; ++j) {
			result[i][j] = 0;
			for (int k = 0; k < 4; ++k)
				result[i][j] += lhs[i][k] * rhs[k][j];
		}
}

export bool MatVecMul(const GzMatrix lhs, GzCoord rhs)
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
