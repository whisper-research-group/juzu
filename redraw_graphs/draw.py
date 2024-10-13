import glob
import json
import os
from multiprocessing import Process

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

Delta_fs = {
    # normal
    "normal/k-g0": 6.667,
    "normal/k-g1": 12.5,
    "normal/kj-gj0": 5.263,
    "normal/kj-gj1": 7.692,
    "normal/p-b0": 5.0,
    "normal/p-b1": 10.0,
    "normal/pj-bj0": 9.091,
    "normal/pj-bj1": 11.111,
    "normal/s-z0": 7.143,
    "normal/s-z1": 8.333,
    "normal/sh-zh0": 5.882,
    "normal/sh-zh1": 2.273,
    "normal/t-d0": 11.111,
    "normal/t-d1": 9.091,
    "normal/tsh-dzh0": 8.333,
    "normal/tsh-dzh1": 7.692,
    # whisper
    "whisper/k-g0": 8.333,
    "whisper/k-g1": 12.5,
    "whisper/kj-gj0": 5.556,
    "whisper/kj-gj1": 16.667,
    "whisper/p-b0": 12.5,
    "whisper/p-b1": 9.091,
    "whisper/pj-bj0": 8.333,
    "whisper/pj-bj1": 10.0,
    "whisper/s-z0": 7.692,
    "whisper/s-z1": 6.25,
    "whisper/sh-zh0": 5.263,
    "whisper/sh-zh1": 6.25,
    "whisper/t-d0": 3.571,
    "whisper/t-d1": 9.091,
    "whisper/tsh-dzh0": 9.091,
    "whisper/tsh-dzh1": 11.111,
}


def draw(
    input_dir,
    output_dir,
    speech_type,
    axis,
):
    json_file_list = glob.glob(input_dir + "/" + "*.json")

    info_dict = {
        "1": {
            "Sf": "60",
            "Sc": "1.2 \\times 10^{-4}",
        },
        "2": {
            "Sf": "60",
            "Sc": "1.5 \\times 10^{-4}",
        },
        "3": {
            "Sf": "60",
            "Sc": "1.8 \\times 10^{-4}",
        },
        "4": {
            "Sf": "70",
            "Sc": "1.2 \\times 10^{-4}",
        },
        "5": {
            "Sf": "70",
            "Sc": "1.5 \\times 10^{-4}",
        },
        "6": {
            "Sf": "70",
            "Sc": "1.8 \\times 10^{-4}",
        },
    }

    process_list = []
    for file in json_file_list:
        process = Process(
            target=plot_graph,
            args=(
                input_dir,
                file,
                axis,
                speech_type,
                output_dir,
                info_dict,
            ),
        )
        process_list.append(process)
        process.start()


def plot_graph(
    input_dir,
    file,
    axis,
    speech_type,
    output_dir,
    info_dict,
):
    Delta_f_key = file.removesuffix(".json")
    if input_dir.endswith("l"):
        Delta_f_key = Delta_f_key.removeprefix(input_dir[:-6])
    elif input_dir.endswith("r"):
        Delta_f_key = Delta_f_key.removeprefix(input_dir[:-7])
    print(input_dir[24], Delta_f_key)
    Delta_f = Delta_fs[Delta_f_key]
    json_open = open(file, "r")
    json_input = json.load(json_open)
    x = []
    y = []
    if axis == "ratio":
        for v in json_input.values():
            x.append(float(v["phi num"]))
            y.append(float(v["cont"]) * 3 / 20)
        x.append(100)
        y.append(0.0)
    elif axis == "hz":
        # Delta_f = json_input["0001"]["freq"] - json_input["0000"]["freq"]
        for v in json_input.values():
            if v["freq"] != 0.0:
                x.append(float(v["freq"]))
                y.append(float(v["cont"]) / Delta_f)
    json_open.close()

    pair_name = os.path.basename(file).removesuffix(".json")
    info = info_dict[input_dir[24]]
    sf = info["Sf"]
    sc = info["Sc"]

    plt.title(f"{speech_type} {pair_name} (average)")
    if axis == "ratio":
        plt.xlabel("Ratio to Fundamental Frequency")
    elif axis == "hz":
        plt.xlabel("Frequency")
    plt.ylabel("Difference in Contribution")

    plt.xscale("log")
    if axis == "ratio":
        plt.xlim(1, 100)
        # plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))
    elif axis == "hz":
        plt.xlim(20, 6000)
        # plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(500))
    plt.ylim(-0.003, 0.003)
    plt.grid(zorder=0)

    if axis == "ratio":
        x = [e + 1 for e in x]
    plt.plot(
        x,
        y,
        color="black",
        linewidth=0.7,
        zorder=2,
    )

    if axis == "hz":
        coefs = np.polyfit(x, y, 10)
        poly = np.poly1d(coefs)
        plt.plot(
            x,
            poly(x),
            color="red",
        )
    if axis == "hz":
        file_name = f"{pair_name}_{speech_type}.jpg"
    else:
        file_name = f"{pair_name}_{speech_type}_{sf}Hz_{sc[0:3]}*10**-4.jpg"

    plt.savefig(
        output_dir + "/" + file_name,
        dpi=800,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.clf()
    plt.close()
