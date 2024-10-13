import finale as fnl

import sys


def main():
    args = sys.argv

    input_dir = args[1]
    speech_type = args[2]
    pair = args[3]
    subject_number = int(args[4])
    fund_approx_fig_file_name = args[5]

    fnl.finale(
        input_dir,

        speech_type,
        pair,

        subject_number,

        fund_approx_fig_file_name,
    )


if __name__ == "__main__":
    main()
