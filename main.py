

def parse_md(filename : str):
	pass



if __name__ == "__main__":
	file = ""
	with open("test.md") as f:
		file = f.read()
	#print(f"{file}")

	# read configs between '&'
	configs = file.split("&&&")[1].split("\n")
	print(f"{configs = }")