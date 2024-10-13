import os
import wave


def main():
    dir_path = "./data-dir/sound-files"
    file_num = 0
    problem = 0

    file_list = []
    dir_list0 = os.listdir(dir_path)
    proc(file_list, dir_path, dir_list0)

    file_list.sort()
    file_count = 0
    for file in file_list:
        wave_file = wave.open(file, mode="rb")
        framerate = wave_file.getframerate()
        if framerate == 16000:
            framerate = f"\033[32m{str(framerate)}\033[m"
        else:
            framerate = f"\033[31m{str(framerate)}\033[m"
            problem += 1
        print(f"{file}: {framerate}")
        file_num += 1
        file_count += 1

        if file.endswith("14.wav"):
            if file_count == 14:
                print(f"\033[32m{file_count}\033[m")
            else:
                print(f"\033[31m{file_count}\033[m")
                problem += 1
            print()
            file_count = 0

    if problem == 0:
        problem = f"\033[32m{str(problem)}\033[m"
    else:
        problem = f"\033[31m{str(problem)}\033[m"

    print(file_num)
    print(f"problem: {problem}")


def proc(file_list, dir_path, dir_list0):
    for dir0 in dir_list0:
        if dir0 != ".DS_Store":
            dir_list1 = os.listdir(f"{dir_path}/{dir0}")
            proc1(file_list, dir_path, dir_list1, dir0)


def proc1(file_list, dir_path, dir_list1, dir0):
    for dir1 in dir_list1:
        if dir1 != ".DS_Store":
            files = os.listdir(f"{dir_path}/{dir0}/{dir1}")
            proc2(file_list, dir_path, dir0, dir1, files)


def proc2(file_list, dir_path, dir0, dir1, files):
    for file in files:
        if file != ".DS_Store":
            file_path = f"{dir_path}/{dir0}/{dir1}/{file}"
            file_list.append(file_path)


if __name__ == "__main__":
    main()
