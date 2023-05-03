from slides import Slides
from config import Config
from renderer import Renderer

PATH_EXAMPLES = "examples"

examples = ["example_nomain.md",
            "example_single_main.md", 
            "example_double_main.md",
            "example_multiple_main_horizontal.md"]

def generate_examples():
    import os
    for example in examples:
        ex = example.split(".")[0]  #  remove file extension

        print(f"Generating {ex} ...")
        s = Slides(f"{PATH_EXAMPLES}/{example}")
        r = Renderer(f"{PATH_EXAMPLES}/{ex}.pdf", s, (1920, 1080))


if __name__ == "__main__":
    generate_examples()
