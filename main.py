class slides:
	def __init__(self, filename : str):
		self.filename = filename
		self.raw = self.__get_raw_md(self.filename)
		self.configs = self.__get_configs(self.raw)
		self.slides = self.__get_slides(self.raw)
		self.html = self.__parse_slides(self.slides)

	def get_html(self, ):
		return self.html

	def __get_raw_md(self, filename : str) -> str:
		import re
		md = ""
		with open(self.filename) as f:
			md = f.read()
		# Clean up a bit
		return re.sub(r'\n+', '\n', md)

	def __get_configs(self, md : str):
		# Skip first --- and empty char
		return list(filter(None, md.split("---")[1].split("\n")))

	def __get_slides(self, md : str) -> list:
		"""
			This gives us a list of every horizontal slides
			Each containing (If there is) sub slides that
			are actually vertical slides
		"""
		# get rid of the config header
		out = "".join(md.split("---")[2:])
		return out.split("-->")

	def __parse_slides(self, s : list) -> str:
		import md_to_reveal as m

		html = ""
		# Col can be multiple vertical slides
		for col in s:
			#print(f"{col = }")
			html += "<section>\n"

			for vslide in col.split("|||"):
				#print(f"{vslide = }")
				html += "\t<section>\n"
				html += m.slide_parser(list(filter(None, vslide.split("\n")))).html
				html += "\t</section>\n"
			html += "</section>\n"
		return html



if __name__ == "__main__":

	s = slides("test.md")

	print(s.get_html())
