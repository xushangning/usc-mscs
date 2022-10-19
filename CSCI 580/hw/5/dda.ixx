export module dda;

import <valarray>;
import <cmath>;
import <numeric>;
import <ranges>;

import "gz.h";

using std::size_t;
using std::valarray;

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
class DDA {
public:
    typedef valarray<valarray<float>> value_type;

private:
    /// <summary>
    /// The index of the element in value_type[0] that is used as the
    /// interpolation parameter e.g., param_index_ == 1 means value_type[0][1]
    /// is the interpolation parameter.
    /// </summary>
    size_t param_index_;

    value_type slope_, value_begin_, value_end_;

public:
    DDA(size_t param_index, const value_type& begin, const value_type& end) noexcept;

    class iterator {
        size_t param_index_;
        value_type value_, slope_;

        iterator(size_t param_index, const value_type& value, const value_type& slope) noexcept
            : param_index_(param_index), value_(value), slope_(slope) {}

    public:
        iterator& operator++() noexcept
        {
            value_ += slope_;
            return *this;
        }

        value_type& operator*() noexcept { return value_; }

        bool operator==(const iterator& other) const noexcept
        {
            return value_[0][param_index_] == other.value_[0][other.param_index_];
        }

        friend class DDA;
    };

    iterator begin() const noexcept { return iterator(param_index_, value_begin_, slope_); }
    iterator end() const noexcept { return iterator(param_index_, value_end_, slope_); }
};

DDA::DDA(size_t param_index, const value_type& begin, const value_type& end) noexcept
    : param_index_(param_index), slope_(end - begin), value_begin_(begin), value_end_(end)
{
    auto initial_param = begin[0][param_index],
        // ceil moves the starting parameter to its next integer.
        param_begin = std::ceil(initial_param),
        delta_param = param_begin - initial_param,
        param_diff = end[0][param_index] - initial_param;

    for (auto& v : slope_)
        v /= param_diff;
    for (size_t i = 0; i < value_begin_.size(); ++i)
        value_begin_[i] += slope_[i] * delta_param;
    value_begin_[0][param_index] = param_begin;

    // Ensure that begin == end when iteration ends.
    value_end_[0][param_index] = std::ceil(value_end_[0][param_index]);
}

constexpr float perspectiveCorrectionCoefficient(float z) noexcept
{
    return z / (static_cast<float>(std::numeric_limits<GzDepth>::max()) - z);
}

DDA::value_type toInterpolationSpace(const DDA::value_type& v) noexcept
{
    auto result = v;
    auto c = perspectiveCorrectionCoefficient(v[0][2]);
    for (auto& x : result | std::views::drop(1))
        x /= c + 1.0f;
    return result;
}

DDA::value_type fromInterpolationSpace(const DDA::value_type& v) noexcept
{
    auto result = v;
    auto c = perspectiveCorrectionCoefficient(v[0][2]);
    for (auto& x : result | std::views::drop(1))
        x *= c + 1.0f;
    return result;
}

/// <summary>
/// DDA with perspective correction. It assumes that the first element of the
/// nested valarray is a 3D coordinate and its z-coordinate is used for
/// perspective correction.
/// </summary>
export class PerspectiveCorrectDDA : public DDA
{
public:
    PerspectiveCorrectDDA(size_t param_index, const value_type& begin, const value_type& end) noexcept
        : DDA(param_index, toInterpolationSpace(begin), toInterpolationSpace(end)) {}

    class iterator : public DDA::iterator
    {
        value_type value_;

        iterator(DDA::iterator&& i) noexcept
            : DDA::iterator(std::move(i)), value_(fromInterpolationSpace(DDA::iterator::operator*())) {}

    public:
        iterator& operator++() noexcept
        {
            DDA::iterator::operator++();
            value_ = fromInterpolationSpace(DDA::iterator::operator*());
            return *this;
        }

        const value_type& operator*() const noexcept { return value_; }

        friend class PerspectiveCorrectDDA;
    };

    iterator begin() const noexcept { return iterator(DDA::begin()); }
    iterator end() const noexcept { return iterator(DDA::end()); }
};
