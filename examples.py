from slides import Slides
from config import Config
from renderer import Renderer

PATH_EXAMPLES = "examples"


examples = ["example_nomain.md"]

def generate_examples():
	import os
	for example in examples:
		#  remove file extension
		ex = example.split(".")[0]

		print(f"Generating {ex} ...")
		s = Slides(f"{PATH_EXAMPLES}/{example}")
		r = Renderer(f"{PATH_EXAMPLES}/{ex}.pdf", s, (1920, 1080))


if __name__ == "__main__":
	generate_examples()