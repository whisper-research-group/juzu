import kazune as kzn
import sys


def main():
    args = sys.argv
    json_file = args[1]
    sentence_type = args[2]
    subject_num = args[3]
    sentence_num = args[4]
    fund_approx_fig_file_name = args[5]

    kazune_formant_num = int(args[6])
    kazune_threshold = int(args[7])
    kazune_error_range = int(args[8])
    kazune_accuracy = int(args[9])

    kzn.kazune(
        json_file,
        sentence_type,
        subject_num,
        sentence_num,
        fund_approx_fig_file_name,

        kazune_formant_num,
        kazune_threshold,
        kazune_error_range,
        kazune_accuracy,
    )


if __name__ == "__main__":
    main()
