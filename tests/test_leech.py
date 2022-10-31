from doofus.leech import _rotate_fields, _table_dict, _calculate_table_diff


def test_rotate_fields():
    table = [
        ["lastname", "firstname", "born"],
        ["harrison", "george", "1943"],
        ["starr", "ringo", "1940"],
        ["lennon", "john", "1940"],
        ["mccartney", "paul", "1942"],
    ]

    test = _rotate_fields("born", table)
    assert test == [
        ["born", "firstname", "lastname"],
        ["1943", "george", "harrison"],
        ["1940", "ringo", "starr"],
        ["1940", "john", "lennon"],
        ["1942", "paul", "mccartney"],
    ]

    test = _rotate_fields(("lastname", "firstname"), table)
    assert test == [
        ["firstname", "lastname", "born"],
        ["george", "harrison", "1943"],
        ["ringo", "starr", "1940"],
        ["john", "lennon", "1940"],
        ["paul", "mccartney", "1942"],
    ]


def test_diff_dict():
    table = [
        ["lastname", "firstname", "born"],
        ["harrison", "george", "1943"],
        ["starr", "ringo", "1940"],
        ["lennon", "john", "1940"],
        ["mccartney", "paul", "1942"],
    ]

    fields, dct = _table_dict(("lastname",), table)
    assert fields == "lastname,born,firstname"
    expect = {
        "harrison": "1943,george",
        "starr": "1940,ringo",
        "lennon": "1940,john",
        "mccartney": "1942,paul",
    }
    assert dct == expect


def test_calculate_diff():
    # No change
    new = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    insertions, deletions, modifications, diff = _calculate_table_diff(
        "sample.csv", "id", new, old
    )
    assert insertions == 0
    assert deletions == 0
    assert modifications == 0
    assert diff == [
        "sample.csv",
        "id,born,firstname,lastname",
    ]

    # Add row
    new = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    insertions, deletions, modifications, diff = _calculate_table_diff(
        "sample.csv", ["id"], new, old
    )
    assert insertions == 1
    assert deletions == 0
    assert modifications == 0
    assert diff == [
        "sample.csv",
        "id,born,firstname,lastname",
        "+1,1940,ringo,starr",
    ]

    # Remove row
    new = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    insertions, deletions, modifications, diff = _calculate_table_diff(
        "sample.csv", ("id", "born"), new, old
    )
    assert insertions == 0
    assert deletions == 1
    assert modifications == 0
    assert diff == [
        "sample.csv",
        "born,id,firstname,lastname",
        "-1940,2",
    ]

    # Change row
    new = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "McCartney", "Paul", "1942"],
    ]
    old = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    insertions, deletions, modifications, diff = _calculate_table_diff(
        "sample.csv", ["id"], new, old
    )
    assert insertions == 0
    assert deletions == 0
    assert modifications == 1
    assert diff == [
        "sample.csv",
        "id,born,firstname,lastname",
        "%3,1942,McCartney,Paul",
    ]

    # Remove, add, change
    new = [
        ["id", "lastname", "firstname", "born"],
        ["0", "harrison", "george", "1943"],
        ["2", "lennon", "john", "1940"],
        ["1", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "lastname", "firstname", "born"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    insertions, deletions, modifications, diff = _calculate_table_diff(
        "sample.csv", ["firstname", "lastname"], new, old
    )
    assert insertions == 1
    assert deletions == 1
    assert modifications == 1
    assert diff == [
        "sample.csv",
        "firstname,lastname,born,id",
        "+george,harrison,1943,0",
        "-ringo,starr",
        "%paul,mccartney,1942,1",
    ]
