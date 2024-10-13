import glob
import json
import os

import matplotlib.pyplot as plt
import numpy as np


def finale(
    input_dir,
    speech_type,
    pair,
    subject_number,
    fund_approx_fig_file_name,
):
    os.chdir(os.environ["HOME"])
    os.chdir(input_dir + "/" + "result2-json" + "/" + speech_type + "/" + pair)

    json_file_list = glob.glob("*.json")

    json_out = {}

    for i in range(0, 100):
        json_out[str(i).zfill(3)] = {
            "cont": 0.0,
            "phi num": str(i).zfill(3),
        }

    cont_list = []

    for i in range(100):
        cont_list.append([])

    for file in json_file_list:
        json_open = open(file, "r")
        json_input = json.load(json_open)
        for i in range(100):
            cont = 0
            if str(i).zfill(3) in json_input:
                cont = json_input[str(i).zfill(3)]["cont"]
            json_out[str(i).zfill(3)]["cont"] += cont
            cont_list[i].append(cont)

    for i in range(100):
        # `subject_number` means how many subjects there are
        json_out[str(i).zfill(3)]["cont"] /= subject_number

    os.chdir(os.environ["HOME"])
    os.chdir(input_dir)

    out_json_file = open(
        "result2-json/" + speech_type + "/" + pair + "/" + "result" + ".json",
        "w",
    )

    json.dump(json_out, out_json_file, indent=4, sort_keys=True)

    x = [i for i in range(100)]
    y = [json_out[str(i).zfill(3)]["cont"] for i in range(100)]
    y_err = [np.std(cont_list[i]) for i in range(100)]

    plt.plot(
        x,
        y,
        color="black",
        linewidth=0.7,
        zorder=2,
    )
    plt.errorbar(
        x,
        y,
        yerr=y_err,
        capsize=1,
        ecolor="#1f77b4",
        fmt="o",
        markersize=0,
        linewidth=0.5,
        capthick=0.5,
        zorder=1,
    )
    plt.xlim(0, 100)
    plt.ylim(-0.1, 0.1)

    plt.title(f"{speech_type} {pair} [average]")
    plt.xlabel("Ratio to Fundamental Frequency")
    plt.ylabel("Intensity of Contribution")
    value_sets = [[x[i], y[i]] for i in range(100)]
    sorted_values = sorted(y)
    important_values = sorted_values[:5] + sorted_values[-5:]
    important_value_sets = []
    for i in range(10):
        for j in range(100):
            if value_sets[j][1] == important_values[i]:
                important_value_sets.append(value_sets[j])
                break

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

    print(f"finale:\tpair=\t{pair}")
