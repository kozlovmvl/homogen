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

    @staticmethod
    def get_det(matrix):
        if len(matrix) == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        temp = 0
        for i, line in enumerate(matrix):
            temp += (-1)**i*line[0]*Form.get_det([line_[1:] for k, line_ in enumerate(matrix) if k != i])
        return temp

    @staticmethod
    def silvestr(matrix):
        if any([line[i] <= 0 for i, line in enumerate(matrix)]):
            return False
        det = matrix[0][0]
        for row in range(1, len(matrix)):
            temp = 0
            for j in range(row):
                temp += (-1)**(row+j)*Form.get_det([line[:j]+line[j+1:] for line in matrix[:row]])
            temp += matrix[row][row]*det
            if temp <= 0:
                return False
            det = temp
        return True

    def __get_matching(self):
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
        num_add = 0
        for item in matching.values():
            if len(item) == 2:
                num_add += 1
        return matching, num_add

    def __get_q_matrix(self, matching):
        q_matrix = [[0 for i in range(self.q_dim)] for j in range(self.q_dim)]
        for old_index, couples in matching.items():
            q_matrix[couples[0][0]][couples[0][1]] = self.coeffs[old_index]
        return q_matrix

    def __get_full_matrix(self, matching, args):
        assert len(args) == self.num_add, ('Length of \'args\' must be equal %s' % self.num_add)
        full_matrix = [[0 for i in range(self.q_dim)] for j in range(self.q_dim)]
        count = 0
        for old_index, couples in matching.items():
            full_matrix[couples[0][0]][couples[0][1]] = self.coeffs[old_index] / 2
            full_matrix[couples[0][1]][couples[0][0]] = self.coeffs[old_index] / 2
            if len(couples) == 2:
                full_matrix[couples[0][0]][couples[0][1]] = args[count] / 2
                full_matrix[couples[0][1]][couples[0][0]] = args[count] / 2
                full_matrix[couples[1][0]][couples[1][1]] = -args[count] / 2
                full_matrix[couples[1][1]][couples[1][0]] = -args[count] / 2
                count += 1
        return full_matrix

    def is_positive(self, radius=1):
        assert not self.deg % 2, ('Degree must be even number')
        assert isinstance(radius, int) or isinstance(radius, float), ('Argument \'radius\' must be '
                                                                      'integer or float number')
        assert radius > 0, ('Argument \'radius\' must be positive')
        self.q_dim = Form.binom(self.dim + self.deg // 2 - 1, self.dim - 1)
        sign = False
        # превращаем в квадратичные формы
        matching, self.num_add = self.__get_matching()
        self.area = [[-radius, radius] for i in range(self.num_add)]
        full_matrix = self.__get_full_matrix(matching, [1,1,1,1,1,1])
        return full_matrix
