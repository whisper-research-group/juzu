import glob
import os
import sys

import kurabe as krb


def main():
    args = sys.argv
    input_dir = args[1]
    work_dir = args[2]
    speech_type = args[3]
    subject_num = args[4]
    pair = args[5]
    fund_approx_fig_file_name = args[6]

    os.chdir(work_dir)
    json_file_list = glob.glob("*.json")
    json_file_list.sort()

    json_file1 = json_file_list[0]
    json_file2 = json_file_list[1]

    print(f"kurabe:\tkurabe2:\tpair=\t{pair}")

    krb.kurabe(
        input_dir,
        json_file1,
        json_file2,
        speech_type,
        subject_num,
        fund_approx_fig_file_name,
    )


if __name__ == "__main__":
    main()
