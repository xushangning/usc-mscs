export module dda;

import <array>;
import <cmath>;

import "gz.h";

using std::size_t;
using std::array;

/// <summary>
/// Digital Differential Analyzer for linear interpolation as a C++ container.
/// For example, given a pair of begin and end coordinates with the y-axis as
/// the interpolation parameter, for each coordinate on the line segment
/// between the begin and end coordinates with integral y, it can linearly
/// interpolate the x and z values. These interpolated coordinates are
/// available as elements in a C++ container.
/// </summary>
/// 
/// <remarks>
/// The contanier follows the left-closed, right-open C++ indexing convention.
/// That is, the begin coordinate is included in the container if its parameter
/// is integral, while the end coordinate is never included.
/// </remarks>
export class DDA {
public:
    typedef array<float, 3> value_type;

private:
    /// <summary>
    /// The index of dimension in a coordinate that is used as the
    /// interpolation parameter e.g., param_index_ == 1 means the y-axis is the
    /// interpolation parameter.
    /// </summary>
    size_t param_index_;

    value_type slope_, value_begin_, value_end_;

public:
    DDA(size_t param_index, const value_type& begin, const value_type& end) noexcept;
    DDA(size_t param_index, const GzCoord& begin, const GzCoord& end) noexcept
        : DDA(param_index, std::to_array(begin), std::to_array(end)) {}

    class iterator {
        size_t param_index_;
        value_type value_, slope_;

        iterator(size_t param_index, const value_type& value, const value_type& slope) noexcept
            : param_index_(param_index), value_(value), slope_(slope) {}

    public:
        iterator& operator++() noexcept
        {
            for (value_type::size_type i = 0; i < value_.size(); ++i)
                value_[i] += slope_[i];
            return *this;
        }

        value_type& operator*() noexcept { return value_; }

        bool operator==(const iterator& other) const noexcept
        {
            return value_[param_index_] == other.value_[other.param_index_];
        }

        friend class DDA;
    };

    iterator begin() const noexcept { return iterator(param_index_, value_begin_, slope_); }
    iterator end() const noexcept { return iterator(param_index_, value_end_, slope_); }
};

DDA::DDA(size_t param_index, const value_type& begin, const value_type& end) noexcept
    : param_index_(param_index), value_end_(end)
{
    auto initial_param = begin[param_index],
        param_begin = std::ceil(initial_param),
        delta_param = param_begin - initial_param,
        param_diff = end[param_index] - initial_param;

    // Move the starting parameter to its next integer.
    for (value_type::size_type i = 0; i < value_begin_.size(); ++i)
        if (i == param_index) {
            slope_[i] = 1;
            value_begin_[i] = param_begin;
        }
        else {
            slope_[i] = (end[i] - begin[i]) / param_diff;
            value_begin_[i] = begin[i] + slope_[i] * delta_param;
        }

    // Ensure that begin == end when iteration ends.
    value_end_[param_index] = std::ceil(value_end_[param_index]);
}
