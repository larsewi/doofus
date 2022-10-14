from doofus.leech import _diff_dict, _calculate_diff

def test_diff_dict():
    table = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    fields, dct = _diff_dict(("id"), table)
    assert fields == "id,firstname,lastname,born"
    expect = {
        "0": "harrison,george,1943",
        "1": "starr,ringo,1940",
        "2": "lennon,john,1940",
        "3": "mccartney,paul,1942",
    }
    assert dct == expect

    table = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    fields, dct = _diff_dict(("firstname", "lastname"), table)
    assert fields == "firstname,lastname,id,born"
    expect = {
        "harrison,george": "0,1943",
        "starr,ringo": "1,1940",
        "lennon,john": "2,1940",
        "mccartney,paul": "3,1942",
    }
    assert dct == expect


def test_calculate_diff():
    # No change
    new = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    diff = _calculate_diff(["id"], new, old)
    expect = ["id,firstname,lastname,born"]
    assert diff == expect

    # Add row
    new = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    diff = _calculate_diff(["id"], new, old)
    expect = ["id,firstname,lastname,born", "+1,starr,ringo,1940"]
    assert diff == expect

    # Remove row
    new = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    diff = _calculate_diff(["id"], new, old)
    expect = ["id,firstname,lastname,born", "-2"]
    assert diff == expect

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
    diff = _calculate_diff(["id"], new, old)
    expect = ["id,firstname,lastname,born", "%3,McCartney,Paul,1942"]
    assert diff == expect

    # Remove, add, change, combined primary key
    new = [
        ["id", "firstname", "lastname", "born"],
        ["0", "harrison", "george", "1943"],
        ["2", "lennon", "john", "1940"],
        ["1", "mccartney", "paul", "1942"],
    ]
    old = [
        ["id", "firstname", "lastname", "born"],
        ["1", "starr", "ringo", "1940"],
        ["2", "lennon", "john", "1940"],
        ["3", "mccartney", "paul", "1942"],
    ]
    diff = _calculate_diff(["firstname", "lastname"], new, old)
    expect = [
        "firstname,lastname,id,born",
        "+harrison,george,0,1943",
        "-starr,ringo",
        "%mccartney,paul,1,1942",
    ]
    assert diff == expect
