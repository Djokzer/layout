class slides:

	def __init__(self, filename : str):
		self.filename = filename
		self.raw = self.__get_raw_md(self.filename)
		self.configs = self.__get_configs(self.raw)
		self.slides = self.__get_slides(self.raw)

	def __get_raw_md(self, filename : str) -> str:
		import re
		md = ""
		with open("test.md") as f:
			md = f.read()

		# Clean up a bit
		return re.sub(r'\n+', '\n', md)

	def __get_configs(self, md : str):
		# Skip first --- and empty char
		return list(filter(None, md.split("---")[1].split("\n")))

	def __get_slides(self, md : str):
		# get rid of the config header
		out = "".join(md.split("---")[2:])
		return out.split("-->")

	def __md_to_header(self, md_title : str):
		c = md_title.count("#")
		return f"<h{c}>{md_title[c+1:]}</h{c}>"


def substr_between(text : str, l : str, r : str) -> str:
	return text[text.index(l)+len(l):text.index(r)]


if __name__ == "__main__":

	s = slides("test.md")

	html = ""
	for hslide in s.slides:
		html += "<section>\n"
		
		vslide = list(filter(None, hslide.split("|||")))
		for item in vslide:
			html += "\t<section>\n"
			for elem in list(filter(None, item.split("\n"))):
				html += f"\t\t{md_to_header(elem)}\n"
			html += "\t</section>\n"
		
		html += "</section>\n"

	print(html)
