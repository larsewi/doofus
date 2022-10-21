from doofus.leech import _rotate_fields, _table_dict, _calculate_table_diff


def test_rotate_fields():
    table = [
        ["lastname", "firstname", "born"],
        ["harrison", "george", "1943"],
        ["starr", "ringo", "1940"],
        ["lennon", "john", "1940"],
        ["mccartney", "paul", "1942"],
    ]

    test =_rotate_fields("lastname", table)
    assert test == table

    test = _rotate_fields("firstname", table)
    expect = [
        ["firstname", "lastname", "born"],
        ["george", "harrison", "1943"],
        ["ringo", "starr", "1940"],
        ["john", "lennon", "1940"],
        ["paul", "mccartney", "1942"],
    ]
    assert test == expect

    test = _rotate_fields("born", table)
    expect = [
        ["born", "lastname", "firstname"],
        ["1943", "harrison", "george"],
        ["1940", "starr", "ringo"],
        ["1940", "lennon", "john"],
        ["1942", "mccartney", "paul"],
    ]
    assert test == expect

    test = _rotate_fields(("lastname", "firstname"), table)
    assert test == table

    test = _rotate_fields(("lastname", "born"), table)
    expect = [
        ["lastname", "born", "firstname"],
        ["harrison", "1943", "george"],
        ["starr", "1940", "ringo"],
        ["lennon", "1940", "john"],
        ["mccartney", "1942", "paul"],
    ]
    assert test == expect

    test = _rotate_fields(("firstname", "born"), table)
    expect = [
        ["firstname", "born", "lastname"],
        ["george", "1943", "harrison"],
        ["ringo", "1940", "starr"],
        ["john", "1940", "lennon"],
        ["paul", "1942", "mccartney"],
    ]

    # Make sure order is kept even though order in first is not kept
    test = _rotate_fields(("lastname", "firstname", "born"), table)
    assert test == table

    test = _rotate_fields(("born", "lastname", "firstname"), table)
    assert test == table

    test = _rotate_fields(("firstname", "born", "lastname"), table)
    assert test == table


def test_diff_dict():
    table = [
        ["lastname", "firstname", "born"],
        ["harrison", "george", "1943"],
        ["starr", "ringo", "1940"],
        ["lennon", "john", "1940"],
        ["mccartney", "paul", "1942"],
    ]

    fields, dct = _table_dict(("lastname",), table)
    assert fields == "lastname,firstname,born"
    expect = {
        "harrison": "george,1943",
        "starr": "ringo,1940",
        "lennon": "john,1940",
        "mccartney": "paul,1942",
    }
    assert dct == expect

    fields, dct = _table_dict(("firstname",), table)
    assert fields == "firstname,lastname,born"
    expect = {
        "george": "harrison,1943",
        "ringo": "starr,1940",
        "john": "lennon,1940",
        "paul": "mccartney,1942",
    }
    assert dct == expect

    fields, dct = _table_dict(("lastname", "firstname"), table)
    assert fields == "lastname,firstname,born"
    expect = {
        "harrison,george": "1943",
        "starr,ringo": "1940",
        "lennon,john": "1940",
        "mccartney,paul": "1942",
    }
    assert dct == expect

    fields, dct = _table_dict(("born", "firstname"), table)
    assert fields == "firstname,born,lastname"
    expect = {
        "george,1943": "harrison",
        "ringo,1940": "starr",
        "john,1940": "lennon",
        "paul,1942": "mccartney",
    }
    assert dct == expect


# def test_calculate_diff():
#     # No change
#     new = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     old = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     diff = _calculate_table_diff(["id"], new, old)
#     expect = ["id,firstname,lastname,born"]
#     assert diff == expect
# 
#     # Add row
#     new = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     old = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     diff = _calculate_table_diff(["id"], new, old)
#     expect = ["id,firstname,lastname,born", "+1,starr,ringo,1940"]
#     assert diff == expect
# 
#     # Remove row
#     new = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     old = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     diff = _calculate_table_diff(["id"], new, old)
#     expect = ["id,firstname,lastname,born", "-2"]
#     assert diff == expect
# 
#     # Change row
#     new = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "McCartney", "Paul", "1942"],
#     ]
#     old = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     diff = _calculate_table_diff(["id"], new, old)
#     expect = ["id,firstname,lastname,born", "%3,McCartney,Paul,1942"]
#     assert diff == expect
# 
#     # Remove, add, change, combined primary key
#     new = [
#         ["id", "firstname", "lastname", "born"],
#         ["0", "harrison", "george", "1943"],
#         ["2", "lennon", "john", "1940"],
#         ["1", "mccartney", "paul", "1942"],
#     ]
#     old = [
#         ["id", "firstname", "lastname", "born"],
#         ["1", "starr", "ringo", "1940"],
#         ["2", "lennon", "john", "1940"],
#         ["3", "mccartney", "paul", "1942"],
#     ]
#     diff = _calculate_table_diff(["firstname", "lastname"], new, old)
#     expect = [
#         "firstname,lastname,id,born",
#         "+harrison,george,0,1943",
#         "-starr,ringo",
#         "%mccartney,paul,1,1942",
#     ]
#     assert diff == expect
