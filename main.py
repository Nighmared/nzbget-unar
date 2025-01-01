import os
import subprocess
import sys

POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95

DIR_KEY = "NZBPP_DIRECTORY"
NZB_NAME_KEY = "NZBPP_NZBNAME"
NZB_FILE_KEY = "NZBPP_NZBFILENAME"


def iprint(*args, **kwargs):
    print("[INFO]", *args, **kwargs)


def eprint(*args, **kwargs):
    print("[ERROR]", *args, **kwargs)


def main():

    try:
        dest_dir = os.environ[DIR_KEY]
        dest_dir_found = True
    except KeyError:
        dest_dir = "dest dir not found"
        dest_dir_found = False

    if not dest_dir_found:
        iprint("exiting with none (??)")
        sys.exit(POSTPROCESS_NONE)

    parsed_path = os.path.normpath(dest_dir)
    listing = os.listdir(parsed_path)
    if len(listing) == 1:
        new_path = os.path.join(parsed_path, listing[0])
        if os.path.isdir(new_path):
            parsed_path = new_path
            listing = os.listdir(parsed_path)

    if len(listing) < 5:
        iprint("Skipping, does not need additional extraction")
        sys.exit(POSTPROCESS_NONE)

    num_to_part_rar_paths: dict[int, str] = {}
    path_list = []
    for f in os.listdir(parsed_path):
        if f[-3] == "r" and (num := f[-2:]).isdigit():
            key = int(num)
            val = os.path.join(parsed_path, f)
            path_list.append(val)
            num_to_part_rar_paths[key] = val

    a = sorted(num_to_part_rar_paths.items(), key=lambda x: x[0])
    cmd = f"unrar x -y {a[0][1]} {parsed_path}"
    retc = subprocess.call(cmd, shell=True)
    if retc != 0:
        eprint(f"Unrar exited with code {retc}")
        sys.exit(POSTPROCESS_ERROR)
    iprint("Successfully extracted from multi-archive")
    rm_cmd = "rm " + (" ".join(path_list))
    retc = subprocess.call(rm_cmd, shell=True)
    if retc != 0:
        eprint(f"Cleanup exited with code {retc}")
        sys.exit(POSTPROCESS_ERROR)
    iprint("Successfully deleted partial RARs")
    sys.exit(POSTPROCESS_SUCCESS)


if __name__ == "__main__":
    main()
