def clean_up(input : str) -> str:
	import re
	return re.sub(r'\n+', '\n', md)

def read_md(filename : str) -> str:
	md = ""
	with open("test.md") as f:
		md = f.read()
	return md

def get_configs(md : str):
	# Skip first --- and empty char
	return list(filter(None, md.split("---")[1].split("\n")))

def get_hslides(md : str):
	# get rid of the config header
	out = "".join(md.split("---")[2:])
	return out.split("-->")

def md_to_header(md_title : str):
	c = md_title.count("#")
	return f"<h{c}>{md_title[c+1:]}</h{c}>"

if __name__ == "__main__":
	md = read_md("test.md")
	md = clean_up(md)
	#print(md)

	# read configs between '&'
	#configs = get_configs(md)
	#print(f"{configs = }\n")

	hslides = get_hslides(md)
	#print(hslides[0])
	print(*hslides, sep="/\n")

	html = ""
	vslides = []
	for hslide in hslides:
		html += "<section>\n"
		vslide = list(filter(None, hslide.split("|||")))
		for item in vslide:
			html += "\t<section>\n"
			for elem in list(filter(None, item.split("\n"))):
				html += f"\t\t{md_to_header(elem)}\n"
			html += "\t</section>\n"
		html += "</section>\n"

	print(html)

	#print(len(vslides))
	#print(*vslides, sep="\n\n")

