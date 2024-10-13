import json
import math
import matplotlib.pyplot as plt


def approximate_formant(
        input_file,
        referencing_formant_number,
        first_step_approximating_threshold,
        second_step_approximating_error_range,
        second_step_approximating_accuracy,
):
    formant_list = import_jsonfile(input_file)
    formant_list = optimize_inputs(formant_list, referencing_formant_number)

    approximated_fundamental1 = \
        first_step_approximated_fundamental(
            formant_list,
            first_step_approximating_threshold,
        )

    reference_formant = approximated_fundamental1
    minimum_error_formant = math.floor(
        reference_formant - second_step_approximating_error_range / 2
    )
    maximum_error_formant = math.ceil(
        reference_formant + second_step_approximating_error_range / 2
    )

    output_approximated_fundamental_list = approximated_fundamental_list(
        formant_list,
        minimum_error_formant,
        maximum_error_formant,
        second_step_approximating_accuracy,
    )

    formant_overtone_difference_sum_square_list = []
    for i in range(len(output_approximated_fundamental_list)):
        formant_overtone_difference_sum_square_list.append(
            output_approximated_fundamental_list[i][1]
        )

    approximated_fundamental2 = \
        output_approximated_fundamental_list[
            formant_overtone_difference_sum_square_list
            .index(min(formant_overtone_difference_sum_square_list))
        ][0]

    output = approximated_fundamental2

    return output


def plot_approximating_fundamentals(
        input_file,
        referencing_formant_number,
        first_step_approximating_threshold,
        second_step_approximating_error_range,
        second_step_approximating_accuracy,
        generated_file_name,
):
    formant_list = import_jsonfile(input_file)
    formant_list = optimize_inputs(formant_list, referencing_formant_number)

    approximated_fundamental1 = \
        first_step_approximated_fundamental(
            formant_list,
            first_step_approximating_threshold,
        )

    reference_formant = approximated_fundamental1
    minimum_error_formant = math.floor(
        reference_formant - second_step_approximating_error_range / 2
    )
    maximum_error_formant = math.ceil(
        reference_formant + second_step_approximating_error_range / 2
    )

    output_approximated_fundamental_list = approximated_fundamental_list(
        formant_list,
        minimum_error_formant,
        maximum_error_formant,
        second_step_approximating_accuracy,
    )

    x = []
    for i in range(len(output_approximated_fundamental_list)):
        x.append(
            output_approximated_fundamental_list[i][0]
        )
    y = []
    for i in range(len(output_approximated_fundamental_list)):
        y.append(
            output_approximated_fundamental_list[i][1]
        )

    plt.plot(x, y)
    plt.savefig(generated_file_name, dpi=300)
    plt.clf()


def import_jsonfile(input_file):
    json_open = open(input_file, "r")
    json_input = json.load(json_open)
    formant_list = \
        [json_input[str(i).zfill(2)]["freq"] for i in range(len(json_input))]

    return formant_list


def approximated_fundamental_list(
        formant_list,
        minimum_error_formant,
        maximum_error_formant,
        second_step_approximating_accuracy,
):
    formant_overtone_difference_list = []
    for i in range(
            minimum_error_formant * 10 ** second_step_approximating_accuracy,
            maximum_error_formant * 10 ** second_step_approximating_accuracy,
    ):
        approximating_fundamental = \
            i * 10 ** (-second_step_approximating_accuracy)
        formant_overtone_difference_list.append(
            [
                approximating_fundamental,
                abs(
                    formant_overtone_difference_sum(
                        formant_list,
                        approximating_fundamental,
                    )
                ),
            ]
        )

    output = formant_overtone_difference_list

    return output


def formant_overtone_difference_sum(formant_list, approximating_fundamental):
    formant_overtone_difference_list = []
    for j in range(len(formant_list)):
        formant_overtone_difference_list.append(
            difference_between_overtone(
                formant_list[j],
                approximating_fundamental,
            )
        )

    output = sum(formant_overtone_difference_list)

    return output


def difference_between_overtone(formant, approximating_fundamental):
    k = 0
    difference_between_overtone1 = formant
    difference_between_overtone2 = 0
    while (
            abs(difference_between_overtone2)
            - abs(difference_between_overtone1)
    ) < 0:
        difference_between_overtone1 = \
            formant - k * approximating_fundamental
        difference_between_overtone2 = \
            formant - (k + 1) * approximating_fundamental
        k += 1

    output = difference_between_overtone1

    return output


def first_step_approximated_fundamental(formant_list, threshold):
    difference_list = formant_list
    while len(difference_list) > 1:
        difference_list = \
            dif_list_for_each_element(difference_list, threshold)

    output = difference_list[0]

    return output


def dif_list_for_each_element(input_list, threshold) -> list:
    difference_list = []
    for i in range(len(input_list) - 1):
        element1 = input_list[i]
        element2 = input_list[i + 1]
        difference = element2 - element1

        if difference < threshold:
            difference_list.append((element1 + element2) / 2)
        else:
            difference_list.append(difference)

    difference_list.sort()

    output = difference_list

    return output


def optimize_inputs(formant_list, referencing_formant_number):
    i = 0
    while i <= len(formant_list) - 1:
        if formant_list[i] < 100:
            formant_list.remove(formant_list[i])
            i -= 1
        i += 1

    del formant_list[referencing_formant_number:]

    output = formant_list

    return output
