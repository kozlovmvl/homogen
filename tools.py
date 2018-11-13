"""
Functional
"""

class Form(object):

    def __init__(self, dim, deg, coeffs=None):
        assert dim > 0 and isinstance(dim, int), ('Argument \'dim\' must be a positive integer')
        assert deg > 0 and isinstance(deg, int), ('Argument \'deg\' must be a positive integer')
        self.dim, self.deg = dim, deg
        self.num_coeffs = Form.binom(dim + deg - 1, deg)
        if coeffs is not None:
            assert isinstance(coeffs, list), ('Argument \'coeffs\' must be a list')
            assert len(coeffs) != self.num_coeffs, ('Length of list \'coeffs\' must be equal %s' % self.num_coeffs)
            assert all(isinstance(c, float) for c in coeffs), ('All coeffs items must have the '
                                                               'type int or float')
        if coeffs:
            self.coeffs = coeffs
        else:
            self.coeffs = list(1 for i in range(self.num_coeffs))

    def __str__(self):
        info = ''
        for attr in ('dim', 'deg', 'num_coeffs', 'coeffs'):
            info += '%s = %s\n' % (attr, self.__getattribute__(attr))
        return info

    @staticmethod
    def binom(n, k):
        if n == 0 or k == 0 or k == n:
            return 1
        return Form.binom(n-1, k) + Form.binom(n-1, k-1)

    @staticmethod
    def gen_monoms(dim, deg):
        list_monoms = []
        def gen(_dim, _deg):
            if _dim == 1:
                return [[_deg]]
            lines = []
            for i in range(_deg+1):
                for li in gen(_dim - 1, i):
                    li.insert(0, _deg - i)
                    lines.append(li)
            if _dim == dim:
                list_monoms.extend([tuple(li) for li in lines])
            return lines
        gen(dim, deg)
        return list_monoms

    def get_matching(self):
        old_monoms = Form.gen_monoms(self.dim, self.deg)
        indexes_old_monoms = {mon: i for i, mon in enumerate(old_monoms)}
        young_monoms = Form.gen_monoms(self.dim, self.deg // 2)
        matching = {}
        for i, mon_1 in enumerate(young_monoms):
            for j, mon_2 in enumerate(young_monoms[i:]):
                old_monom = tuple(el + mon_2[k] for k, el in enumerate(mon_1))
                try:
                    matching[indexes_old_monoms[old_monom]].append((i, j))
                except KeyError:
                    matching[indexes_old_monoms[old_monom]] = [(i, j)]
        return matching

    def is_positive(self):
        assert not self.deg % 2, ('Degree must be even number')
        sign = False
        # превращаем в квадратичные формы

        return bool(sign)