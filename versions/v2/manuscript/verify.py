import hashlib
import json
from math import comb


def multiply(left, right, degree):
    product = [0] * (degree + 1)
    for left_degree, left_value in enumerate(left[:degree + 1]):
        if left_value:
            for right_degree, right_value in enumerate(right[:degree + 1 - left_degree]):
                if right_value:
                    product[left_degree + right_degree] += left_value * right_value
    return product


def compose(outer, inner, degree):
    assert inner[0] == 0
    result = [0] * (degree + 1)
    power = [1] + [0] * degree
    for exponent in range(min(len(outer), degree + 1)):
        if outer[exponent]:
            result = [value + outer[exponent] * term for value, term in zip(result, power)]
        power = multiply(power, inner, degree)
    return result


def subtract_square(series, scalar, degree):
    squared = multiply(series, series, degree)
    return [value - scalar * term for value, term in zip(series, squared)]


def valuation_two(value):
    assert value != 0
    value = abs(value)
    return (value & -value).bit_length() - 1


def calculate(degree=80, parameter=5):
    assert degree >= 2 and (parameter - 1) % 4 == 0
    catalan = [0] + [comb(2 * index - 2, index - 1) // index for index in range(1, degree + 1)]
    identity = [0, 1] + [0] * (degree - 1)
    direct = identity.copy()
    for index in range(2, degree + 1):
        inner = subtract_square(direct[:index + 1], 1, index)
        residual = compose(direct[:index + 1], inner, index)[index]
        numerator = parameter ** (index - 1) * catalan[index] - residual
        assert numerator % 2 == 0
        direct[index] = numerator // 2
    root = identity.copy()
    target = [parameter * value + (1 - parameter) * term for value, term in zip(identity, catalan)]
    for index in range(2, degree + 1):
        residual = compose(root[:index + 1], root[:index + 1], index)[index] - target[index]
        assert residual % 4 == 0
        root[index] = -residual // 2
    inverse = identity.copy()
    for index in range(2, degree + 1):
        inverse[index] = -compose(root[:index + 1], inverse[:index + 1], index)[index]
    constructed = compose(catalan, inverse, degree)
    assert direct == constructed
    assert compose(root, root, degree) == target
    assert compose(root, inverse, degree) == identity
    assert compose(inverse, root, degree) == identity
    squared = multiply(direct, direct, degree)
    assert direct == [value + parameter * term for value, term in zip(root, squared)]
    inner = subtract_square(direct, 1, degree)
    assert compose(root, inner, degree) == identity
    weighted_catalan = [0] + [parameter ** (index - 1) * catalan[index] for index in range(1, degree + 1)]
    assert compose(weighted_catalan, root, degree) == direct
    assert compose(direct, inner, degree) == weighted_catalan
    assert compose(catalan, inner, degree) == direct
    assert compose(direct, root, degree) == catalan
    modulus = abs((parameter + 1) // 2)
    assert modulus > 0 and modulus % 2 == 1
    for index in range(2, degree + 1):
        assert root[index] % 2 == 0
        assert inverse[index] % 2 == 0
        assert valuation_two(catalan[index]) == index.bit_count() - 1
    for index in range(1, degree + 1):
        power_of_two = index & (index - 1) == 0
        assert direct[index] % 2 == int(power_of_two)
        if index > 1 and parameter == 5:
            assert direct[index] % 6 not in (1, 5)
        if index % 2 == 0:
            assert direct[index] % modulus == 0
            assert direct[index] % (2 * modulus) == (modulus if power_of_two else 0)
    negative_indices = [index for index in range(1, degree + 1) if direct[index] < 0]
    if parameter == 5 and degree >= 58:
        assert negative_indices[0] == 58
    digest = hashlib.sha256(json.dumps(direct, separators=(',', ':')).encode()).hexdigest()
    summary = {
        'parameter': parameter,
        'degree': degree,
        'arithmetic': 'exact integers',
        'coefficient_constructions': ['triangular recurrence', 'integral compositional square root'],
        'constructions_agree': True,
        'functional_identities_1_to_6': True,
        'parity_power_of_two': True,
        'even_index_modulus': 2 * modulus,
        'even_index_residue_classification': True,
        'companion_root_and_inverse_parity': True,
        'coefficients_sha256': digest,
    }
    if parameter == 5:
        expected_terms = [1, 3, 22, 219, 2530, 31830, 422652, 5820099,
                          82226522, 1183598754, 17277560996, 254957527134,
                          3795103401236, 56900877433356, 858486641574392,
                          13025190180880851, 198640087778490698,
                          3043793354165966442, 46845889623804326292,
                          723896233987491887466, 11227150555314722435580]
        assert degree >= len(expected_terms)
        assert direct[1:len(expected_terms) + 1] == expected_terms
        displayed_examples = [
            (catalan, [1, 1, 2, 5, 14, 42, 132]),
            (squared, [0, 1, 6, 53, 570, 6858, 88476, 1195565,
                       16684770, 238312766, 3462822372]),
            (inverse, [1, 2, 16, 166, 1960, 24972, 334176, 4624534,
                       65541752, 945285988]),
            (weighted_catalan, [1, 5, 50, 625, 8750, 131250, 2062500]),
            (root, [1, -2, -8, -46, -320, -2460, -19728, -157726,
                    -1197328, -7965076, -36550864, 79262804]),
            (target, [1, -4, -8, -20, -56, -168, -528, -1716]),
        ]
        for series, expected in displayed_examples:
            assert series[1:len(expected) + 1] == expected
        inverse_square = compose(inverse, inverse, degree)
        weighted_square = multiply(weighted_catalan, weighted_catalan, degree)
        assert inverse_square == [value + 4 * term for value, term in zip(identity, weighted_square)]
        for index in range(2, degree + 1):
            power_of_two = index & (index - 1) == 0
            assert squared[index] % 2 == int(power_of_two)
            assert target[index] == -4 * catalan[index] < 0
            assert inverse_square[index] == 4 * 5 ** (index - 2) * catalan[index] > 0
            assert valuation_two(target[index]) == index.bit_count() + 1
            assert valuation_two(inverse_square[index]) == index.bit_count() + 1
        summary.update({
            'even_index_divisibility_by_three': True,
            'even_index_modulo_six_classification': True,
            'modulo_six_exclusion': True,
            'displayed_sequence_terms': len(expected_terms),
            'displayed_companion_coefficients': sum(len(expected) for series, expected in displayed_examples) - 1,
            'companion_square_signs_and_valuations': True,
            'first_negative_index': negative_indices[0] if negative_indices else None,
            'first_negative_value': direct[negative_indices[0]] if negative_indices else None,
        })
    return direct, summary


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run Python with assertions enabled')
    coefficients, summary = calculate()
    summary['parameter_family'] = {
        'through_degree': 24,
        'samples': [calculate(24, 1 + 4 * parameter_index)[1] for parameter_index in range(-3, 6)],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
