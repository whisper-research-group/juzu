import numpy as np
from pydub import AudioSegment


def dft(input_file):
    source_audio = AudioSegment.from_file(input_file, "wav")

    channels = source_audio.channels
    frame_rate = source_audio.frame_rate
    duration = source_audio.duration_seconds

    signal_array = np.array(source_audio.get_array_of_samples())
    sampling_rate = 1.0/source_audio.frame_rate

    sample_size = len(signal_array)
    coefficient_array = np.fft.fft(signal_array)[0:sample_size//2]
    frequency_array = \
        np.fft.fftfreq(sample_size, sampling_rate)[:sample_size//2]
    
    coefficient_array = np.abs(coefficient_array) / sample_size

    return \
    (
        channels,
        frame_rate,
        duration,

        frequency_array,
        coefficient_array,
    )


def to_one_list(frequency_array, coefficient_array):
    out_list = []
    for i in range(len(frequency_array)):
        out_list.append([frequency_array[i], coefficient_array[i]])
    
    return out_list


def sort_by_hz(input_list):
    if len(input_list) < 1:
        return input_list

    pivot = input_list[0]
    left = []
    right = []

    for x in range(1, len(input_list)):
        if input_list[x][0] <= pivot[0]:
            left.append(input_list[x])
        else:
            right.append(input_list[x])

    left = sort_by_hz(left)
    right = sort_by_hz(right)
    foo = [pivot]

    return left + foo + right


def remove_occurrence(
        min_freq_dif,
        input_freq,
        next_input_freq,
        
        min_coef_dif,
        input_coef,
        next_input_coef,
):
    case1 = (input_freq - next_input_freq) ** 2 < min_freq_dif ** 2
    case2 = (input_coef - next_input_coef) ** 2 < min_coef_dif ** 2

    output = case1 or case2

    return output
