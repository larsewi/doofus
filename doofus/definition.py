from doofus.leech import LCH_Table, LCH_Instance
from doofus.utils import work_dir

def create_leech_instance():
    table = LCH_Table("id", "sample.csv", "sample.dest.csv")
    instance = LCH_Instance(work_dir(), [table])
    return instance
