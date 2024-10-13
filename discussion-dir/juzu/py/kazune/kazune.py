import json
import os

import apxTools as apxT

"""
- Kazune -

Kazune overtonizes formant data given in JSON format.
"""


def kazune(
    json_file,
    speech_type,
    subject_num,
    sentence_num,
    fund_approx_fig_file_name,
    kazune_formant_num,
    kazune_threshold,
    kazune_error_range,
    kazune_accuracy,
):
    phi0 = apxT.approximate_formant(  # calculate the phi0 value here
        input_file=json_file,
        referencing_formant_number=kazune_formant_num,
        first_step_approximating_threshold=kazune_threshold,
        second_step_approximating_error_range=kazune_error_range,
        second_step_approximating_accuracy=kazune_accuracy,
    )

    apxT.plot_approximating_fundamentals(
        input_file=json_file,
        referencing_formant_number=6,
        first_step_approximating_threshold=60,
        second_step_approximating_error_range=10,
        second_step_approximating_accuracy=3,
        generated_file_name=fund_approx_fig_file_name,
    )

    file_name = os.path.basename(json_file).removesuffix(".json")
    data_info = f"{speech_type} {subject_num} {sentence_num} {file_name}"

    print(f"kazune:\t[{data_info}]:\tphi0=\t{round(phi0, 3)}")

    json_out = make_json_out(phi0, 120)  # making an output here

    json_open = open(json_file, "r")
    json_input = json.load(json_open)

    for i in range(len(json_out)):
        phi = json_out[str(i).zfill(3)]
        for j in range(len(json_input)):
            formant_freq = json_input[str(j).zfill(2)]["freq"]
            min_phi = phi["phi range"]["min"]
            max_phi = phi["phi range"]["max"]
            if min_phi <= formant_freq < max_phi:
                formant_cont = json_input[str(j).zfill(2)]["cont"]
                phi["freq"] = formant_freq
                phi["cont"] = formant_cont

                freq = "{:.3f}".format(formant_freq).zfill(8)
                cont = "{:.5f}".format(formant_cont)
                phi_num = str(i - 2).zfill(3)

                print(f"kazune:\t[{data_info}]:\tphi{phi_num} freq=\t{freq}")
                print(f"kazune:\t[{data_info}]:\tphi{phi_num} cont=\t{cont}")
        if phi["freq"] == "null":
            del json_out[str(i).zfill(3)]

    out_json_file = open(  # saved into this location
        "overtones-json/"
        + speech_type
        + "/"
        + subject_num
        + "/"
        + sentence_num
        + "/"
        + file_name
        + ".json",
        "w",
    )

    json.dump(json_out, out_json_file, indent=4, sort_keys=True)


"""
{
    "000":
    {
        "phi num": "-02",
        "phi range":
        {
            "min": 0,
            "max": 0,
        },
        "freq": 0,
        "cont": 0,
    }
}
"""


def make_json_out(phi0, max_phinum):
    json_out = {}

    half_phi0 = phi0 / 2
    for i in range(-2, max_phinum):
        label_num = str(i + 2).zfill(3)
        min_phi = phi0 * (i + 1) - half_phi0
        max_phi = phi0 * (i + 1) + half_phi0
        json_out[label_num] = {
            "phi num": str(i).zfill(3),
            "phi range": {
                "min": min_phi,
                "max": max_phi,
            },
            "freq": "null",
            "cont": "null",
        }

    return json_out
