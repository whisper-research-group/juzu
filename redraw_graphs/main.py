import redraw_graphs.draw as draw

# draw(
#     input_dir,
#     output_dir,
#     speech_type,
#     axis,
# )


def main():
    dir_list = [
        # "discussion-dir-07272024-1",
        # "discussion-dir-07272024-2",
        # "discussion-dir-07272024-3",
        # "discussion-dir-07272024-4",
        # "discussion-dir-07272024-5",
        # "discussion-dir-07272024-6",
    ]

    for dir in dir_list:
        for type in ["normal", "whisper"]:
            input_dir = f"{dir}/formant-ratio/final-output-json/{type}"
            output_dir = "result-ratio"
            draw.draw(
                input_dir,
                output_dir,
                type,
                "ratio",
            )

    for type in ["normal", "whisper"]:
        input_dir = f"discussion-dir-07272024-1/Hz/final-output-json/{type}"
        output_dir = "result-hz"
        draw.draw(
            input_dir,
            output_dir,
            type,
            "hz",
        )


if __name__ == "__main__":
    main()
