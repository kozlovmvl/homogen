"""
Testing
"""

import json
import unittest

from tools import Form


class TestForm(unittest.TestCase):

    def test_is_positive(self):
        with open('forms.json', 'r') as f:
            data = json.loads(f.read())
        results = []
        for item in data:
            form = Form(dim=item['dim'], deg=item['deg'], coeffs=item['coeffs'])
            results.append(form.is_positive() is item['is_positive'])
        self.assertTrue(all(results))


if __name__ == '__main__':
    unittest.main()
    # print(Form.gen_monoms(2, 6))
