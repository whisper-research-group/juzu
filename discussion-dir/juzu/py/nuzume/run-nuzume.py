import json
import os
import sys

import matplotlib.pyplot as plt
import nuzume as nzm


def main():
    sys.setrecursionlimit(10000)
    args = sys.argv

    dir_name = args[1]
    sentence_type = args[2]
    subject_num = args[3]
    sentence_num = args[4]

    minimum_audible_frequency = int(args[5])
    maximum_audible_frequency = int(args[6])

    minimum_frequency_difference = float(args[7])
    minimum_contribution_difference = float(args[8])
    output_formant_number = int(args[9])

    file_list = os.listdir(dir_name)

    for file_name in file_list:
        file_path = dir_name + file_name
        file_name = file_name.removesuffix(".wav")
        uzume_list = nzm.uzume(
            input_file=file_path,
            min_audible_freq=minimum_audible_frequency,
            max_audible_freq=maximum_audible_frequency,
            min_freq_difference=minimum_frequency_difference,
            min_cont_difference=minimum_contribution_difference,
            out_formant_num=output_formant_number,
        )

        x = [uzume_list[i][0] for i in range(len(uzume_list))]
        y = [uzume_list[i][1] for i in range(len(uzume_list))]
        plt.plot(x, y)
        plt.xlim(0, 10000)
        plt.ylim(0, 0.5)
        plt.savefig(
            f"formants-fig/"
            + sentence_type
            + "/"
            + subject_num
            + "/"
            + sentence_num
            + "/"
            + file_name
            + ".jpg",
            format="jpg",
            dpi=300,
        )
        plt.clf()

        json_file = open(
            f"formants-json/"
            + sentence_type
            + "/"
            + subject_num
            + "/"
            + sentence_num
            + "/"
            + file_name
            + ".json",
            "w",
        )

        data_info = f"{sentence_type} {subject_num} {sentence_num} {file_name}"
        print(f"nuzume:\t[{data_info}]:\tuzuming")

        json_out = {}
        for i in range(len(uzume_list)):
            json_out[str(i).zfill(2)] = {
                "freq": uzume_list[i][0],
                "cont": uzume_list[i][1],
            }

            freq = json_out[str(i).zfill(2)]["freq"]
            freq = "{:.3f}".format(freq).zfill(8)
            cont = json_out[str(i).zfill(2)]["cont"]
            cont = "{:.5f}".format(cont)

            print(f"nuzume:\t[{data_info}]:\tfreq=\t{freq}")
            print(f"nuzume:\t[{data_info}]:\tcont=\t{cont}")

        print(f"nuzume:\t[{data_info}]:\tuzumed")
        json.dump(json_out, json_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
