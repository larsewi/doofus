class Table:
    def __init__(self, primary: set, table: list[list]):
        assert all(key in table[0] for key in primary), "Primary key not in table header"
        primary = sorted(primary)

        sorted_primary_indecies = [table[0].index(element) for element in sorted(table[0]) if element in primary]
        sorted_other_indecies = [table[0].index(element) for element in sorted(table[0]) if element not in primary]
        self._data = {}

        for row in table[1:]:
            key = tuple(row[i] for i in sorted_primary_indecies)
            val = tuple(row[i] for i in sorted_other_indecies)
            self._data[key] = val

    def __sub__(self, other):
