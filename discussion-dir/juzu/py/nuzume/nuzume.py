import dftTools as dftT


def uzume(
    input_file,
    min_audible_freq,
    max_audible_freq,
    min_freq_difference,
    min_cont_difference,
    out_formant_num,
):
    (_, _, _, frequency_array, coefficient_array) = dftT.dft(input_file)

    freq_coef_list = dftT.to_one_list(frequency_array, coefficient_array)
    sorted_list = dftT.sort_by_hz(freq_coef_list)

    coef_sum = 0.0
    for i in range(len(sorted_list)):
        coef_sum += sorted_list[i][1]

    for i in range(len(sorted_list)):
        sorted_list[i][1] /= coef_sum

    i = 0
    end_proc = False
    while not end_proc:
        frequency = sorted_list[i][0]
        cont = sorted_list[i][1]

        next_frequency = sorted_list[i + 1][0]
        next_cont = sorted_list[i + 1][1]

        if frequency < min_audible_freq or max_audible_freq < frequency:
            sorted_list.remove(sorted_list[i])
        elif dftT.remove_occurrence(
            min_freq_difference,
            frequency,
            next_frequency,
            min_cont_difference,
            cont,
            next_cont,
        ):
            if cont < next_cont:
                sorted_list.remove(sorted_list[i])
            else:
                sorted_list.remove(sorted_list[i + 1])

        else:
            i += 1

        if i == len(sorted_list) - 1:
            end_proc = True

    if len(sorted_list) < out_formant_num:
        out_formant_num = len(sorted_list)

    formants_freq_and_cont_list = []
    for i in range(out_formant_num):
        formant_freq = round(sorted_list[i][0], 3)
        formant_cont = sorted_list[i][1]

        formants_freq_and_cont = [formant_freq, formant_cont]
        formants_freq_and_cont_list.append(formants_freq_and_cont)

    return formants_freq_and_cont_list
