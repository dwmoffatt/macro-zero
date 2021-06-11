"""
Used to increase the version of the application
"""
import argparse

VERSION_VAR = "__version__"
MINOR_MIN = 0
MINOR_MAX = 99
MAJOR_MIN = 0
MAJOR_MAX = 999

if __name__ in "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Increase version by 1", action="store_true")
    parser.add_argument("--major", help="Increase major by 1", action="store_true")
    parser.add_argument("--minor", help="Increase minor by 1", action="store_true")
    args = parser.parse_args()

    file_string_list = list()
    if args.version or args.major or args.minor:
        with open("../src/modules/__init__.py", "r") as f:
            file_string_list = f.readlines()

        for i in range(0, len(file_string_list)):
            if VERSION_VAR in file_string_list[i]:
                split_line = file_string_list[i].split('"')
                version_value = split_line[1]
                version_value_split = version_value.split(".")

                new_minor_value = int(version_value_split[2])
                new_major_value = int(version_value_split[1])
                new_version_value = int(version_value_split[0])

                if args.version:
                    new_version_value += 1
                    new_major_value = MAJOR_MIN
                    new_minor_value = MINOR_MIN
                if args.major:
                    new_major_value += 1
                    new_minor_value = MINOR_MIN

                    if new_major_value > MAJOR_MAX:
                        new_version_value += 1
                        new_major_value = MAJOR_MIN
                if args.minor:
                    new_minor_value += 1

                    if new_major_value > MINOR_MAX:
                        new_major_value += 1
                        new_minor_value = MINOR_MIN

                file_string_list[i] = f'{VERSION_VAR} = "{new_version_value}.{new_major_value}.{new_minor_value}"\n'

        new_file_contents = "".join(file_string_list)

        with open("../src/modules/__init__.py", "w") as f:
            f.write(new_file_contents)

    else:
        print("----- No valid versioning options specified. File left unchanged!! -----")
