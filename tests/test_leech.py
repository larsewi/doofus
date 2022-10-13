from doofus.leech import _calculate_diff

def test_calculate_diff():
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
    expect = [f"+{'1'}:{'starr,ringo,1949'}"]
    assert diff == expect