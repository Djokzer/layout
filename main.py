from slides import slides
from config import Config
from slides import slides

def main():
	s = slides("simple.md")
	configs, ps = s.get()
	print(f"PARAGRAPHS :  {ps[1].paragraphs}")
	print(f"TITLES  : {ps[1].titles}")
	print(f"CODE    : {ps[1].code}")
	print(configs)

if __name__ == "__main__":
	main()