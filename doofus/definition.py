from doofus.leech import LCH_Table, LCH_Instance

def create_leech_instance():
    table = LCH_Table("id", "sample.csv", "sample.dest.csv")
    instance = LCH_Instance([table])
    return instance
