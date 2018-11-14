"""
Testing
"""


from tools import Form


if __name__ == '__main__':
    # create object form
    # form = Form(dim=3, deg=4)
    # matrix = form.is_positive()
    # for line in matrix:
    #     print(line)
    print(Form.get_det([[1,2,3], [4,5,6], [7,8,9]]))
