from pydub import AudioSegment

"""
- Fuzuki Python -

Fuzuki Python is a part of Fuzuki which python is used.
she cuts a WAV formed sound file into given phonemes.
phonemes are given to her from .txt files in data-dir/transcription-files/*.txt.
"""


def fuzuki(file_name):
    open_seg = open(f"{file_name}.txt")
    seg_text = open_seg.read()
    seg_list = seg_text.split("\n")

    for i in range(len(seg_list)):
        seg_list[i] = seg_list[i].split(" ")

    seg_list.remove([""])

    mora_list = []
    for i in range(len(seg_list)):
        phone = seg_list[i][2]

        if (
            phone == "p"
            or phone == "b"
            or phone == "py"
            or phone == "by"
            or phone == "t"
            or phone == "d"
            or phone == "k"
            or phone == "g"
            or phone == "ky"
            or phone == "gy"
            or phone == "ts"
            or phone == "ch"
            or phone == "j"
            or phone == "s"
            or phone == "z"
            or phone == "sh"
        ):
            mora_list.append([seg_list[i], seg_list[i + 1]])

    sound_file = AudioSegment.from_file(f"{file_name}.wav", format="wav")

    for i in range(len(mora_list)):
        start = float(mora_list[i][0][0]) * 1000
        end = float(mora_list[i][1][1]) * 1000
        consonant = mora_list[i][0][2]
        vowel = mora_list[i][1][2]
        if len(vowel) >= 2 and vowel[1] == ":":
            vowel = vowel[0] * 2

        mora = consonant + vowel

        cut_sound = sound_file[start:end]
        out_file_name = str(i + 1).zfill(2) + mora

        cut_sound.export(f"{out_file_name}.wav", format="wav", bitrate="16k")
        cut_sound.export(f"{out_file_name}.wav", format="wav", bitrate="16k")
