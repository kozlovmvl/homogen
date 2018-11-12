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

    def is_positive(self):
        sign = False
        # превращаем в квадратичные формы

        return bool(sign)