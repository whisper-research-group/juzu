import json
import os

import matplotlib.pyplot as plt


def kurabe(
    input_dir,
    json_file1,
    json_file2,
    speech_type,
    subject_num,
    fund_approx_fig_file_name,
):
    json_open1 = open(json_file1, "r")
    json_open2 = open(json_file2, "r")

    json_input1 = json.load(json_open1)
    json_input2 = json.load(json_open2)

    max_phinum = max(
        int(
            json_input1[
                str(max([int(key) for key in json_input1.keys()])).zfill(3)
            ]["phi num"]
        ),
        int(
            json_input2[
                str(max([int(key) for key in json_input2.keys()])).zfill(3)
            ]["phi num"]
        ),
    )

    json_out = {}

    for i in range(0, max_phinum):
        unvoiced = {
            "phi num": str(i).zfill(3),
            "cont": 0.0,
        }
        voiced = {
            "phi num": str(i).zfill(3),
            "cont": 0.0,
        }

        if str(i).zfill(3) in json_input1:
            unvoiced["cont"] = json_input1[str(i).zfill(3)]["cont"]
        if str(i).zfill(3) in json_input2:
            voiced["cont"] = json_input2[str(i).zfill(3)]["cont"]

        json_out[str(i).zfill(3)] = {
            "phi num": str(i).zfill(3),
            "cont": unvoiced["cont"] - voiced["cont"],
        }

    file_name = os.path.basename(os.getcwd())

    os.chdir(os.environ["HOME"])
    os.chdir(input_dir)

    out_json_file = open(
        "result1-json/"
        + speech_type
        + "/"
        + subject_num
        + "/"
        + file_name
        + ".json",
        "w",
    )

    json.dump(json_out, out_json_file, indent=4, sort_keys=True)

    x = [i for i in range(100)]
    y = []
    for i in range(100):
        if str(i).zfill(3) in json_out:
            y.append(json_out[str(i).zfill(3)]["cont"])
        else:
            y.append(0.0)

    plt.plot(x, y)
    plt.xlim(0, 100)
    plt.ylim(-0.1, 0.1)

    plt.title(f"{speech_type} {os.path.basename(input_dir)} {subject_num}")
    plt.xlabel("Ratio to Fundamental Frequency")
    plt.ylabel("Intensity of Contribution")

    value_sets = [[x[i], y[i]] for i in range(100)]
    sorted_values = sort_xy(value_sets)
    for i in range(10):
        if sorted_values[i][0] < 0:
            del sorted_values[i]

    important_value_sets = sorted_values[:5] + sorted_values[-5:]

    for i in range(10):
        plt.text(
            x=important_value_sets[i][0],
            y=important_value_sets[i][1],
            s=f"$\u03d5_{{{important_value_sets[i][0]}}}$"
            + "="
            + "{:.2e}".format(important_value_sets[i][1]),
            size=2,
            fontstyle="italic",
            horizontalalignment="left",
            verticalalignment="center",
            color="#d62728",
            zorder=3,
        )

    plt.savefig(
        fund_approx_fig_file_name, dpi=800, bbox_inches="tight", pad_inches=0
    )
    plt.clf()


def sort_xy(xy_list):
    if len(xy_list) <= 1:
        return xy_list

    pivot = xy_list.pop(0)

    left = [xy for xy in xy_list if xy[0] <= pivot[0]]
    right = [xy for xy in xy_list if xy[0] > pivot[0]]

    left = sort_xy(left)
    right = sort_xy(right)

    return left + [pivot] + right
