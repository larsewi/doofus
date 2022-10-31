from doofus.leech import LCH_Table, LCH_Instance
from doofus.utils import work_dir


def create_leech_instance():
    table1 = LCH_Table(("lastname", "firstname"), "beatles.csv", "beatles.dest.csv")
    table2 = LCH_Table("id", "pinkfloyd.csv", "pinkfloyd.dest.csv")
    instance = LCH_Instance(work_dir(), [table1, table2])
    return instance
