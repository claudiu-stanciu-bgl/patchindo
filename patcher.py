import glob

import psycopg2
import pickle


class ConnectionParams(object):
    def __init__(self, dbname, host, user, password, port):
        self.dbname = dbname
        self.host = host
        self.user = user
        self.password = password
        self.port = port


class DbState:
    def __init__(self, patch_ver, conn_params):
        self.patch_ver = patch_ver
        self.connection_params = conn_params


def get_sql_scripts(patch_dir):
    return glob.glob(patch_dir + "/*.sql")


def run_sql(dbname, host, user, password):
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=5432)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(open("schema.sql", "r").read())
    except:
        print("I am unable to connect to the database")


def contains(phrase, word):
    if word in phrase:
        return True
    return False


def get_patches(sql_files):
    check_word = "rollback"
    return list(filter(lambda x: not contains(x, check_word), sql_files))


def get_rollbacks(sql_files):
    check_word = "rollback"
    return list(filter(lambda x: contains(x, check_word), sql_files))


def get_patch_ver(filename):
    return int(filename.split("/")[-1].split(".")[0].split("_")[0])


def sort_patches(files, reverse=False):
    files.sort(key=get_patch_ver, reverse=reverse)
    return files


def execute_script(script):
    return True


def apply_patches(files, rollback=False):
    """
    Apply patches
    :param files: sql scripts to apply
    :param rollback: boolean if rollback existing patches (True) or apply patches (False)
    :return: last applied patch version
    """
    nb_files = len(files)
    files = sort_patches(files, reverse=rollback)
    for i in range(0, nb_files):
        is_executed = execute_script(files[i])
        if not is_executed:
            print("failed to apply patch: " + files[i])
            return get_patch_ver(files[i])
    return get_patch_ver(files[i])


def main():
    print("Started")
    dir = "/Users/claudiustanciu/repositories/patchindo/sql"
    scripts = get_sql_scripts(dir)
    patches = get_patches(scripts)
    print("-- patch --")
    print(*patches, sep="\n")
    patches = sort_patches(files=patches, reverse=False)
    print("-- sorted patch --")
    print(*patches, sep="\n")
    # rollbacks = get_rollbacks(scripts)
    # rollbacks.sort(reverse=True)
    # print("-- rollback --")
    # print(*rollbacks, sep="\n")
    # print(get_patch_ver()


if __name__ == "__main__":
    main()
