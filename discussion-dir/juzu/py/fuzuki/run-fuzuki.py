import fuzuki as fzk
import sys


def main():
    args = sys.argv
    file_name = args[1]

    fzk.fuzuki(file_name)
    

if __name__ == "__main__":
    main()
