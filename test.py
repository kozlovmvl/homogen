"""
Testing
"""


from tools import Form


if __name__ == '__main__':
    # create object form
    form = Form(dim=2, deg=4, coeffs=[1, 0, 2, 0, 2])
    print(form.is_positive(radius=2))
