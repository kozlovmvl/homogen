"""
Testing
"""


from tools import Form


if __name__ == '__main__':
    # create object form
    form = Form(dim=3, deg=4)
    print(form.get_matching())
