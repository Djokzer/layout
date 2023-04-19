class Slide:
    
	def __init__(self, slide : str) -> None:
		self.titles = []
		self.paragraphs = []
		self.olists = []
		self.ulists = []
		self.images = []
		self.links = []
		self.code = []
		self.parse(slide)
		print("DEBUG : Slide parsed")
		#print(f"{self.titles=}")

	def parse(self, slide : str) -> None:
		"""
			Parse a slide and fill the attributes
			args:
				slide (str) : slide to parse
			returns:
				None
		"""
		# Split the slide into lines and remove empty lines
		lines = list(filter(None, slide.split("\n")))

		for line in lines:
			if self.__is_title(line):
				self.titles.append(line)
			elif self.__is_image(line):
				self.images.append(line)
			elif self.__is_link(line):
				self.links.append(line)
			elif self.__is_code(line):
				self.code.append(line)
			elif self.__is_olist(line):
				self.olists.append(line)
			elif self.__is_ulist(line):
				self.ulists.append(line)
			elif self.__is_sublist(line):
				self.ulists.append(line)
			elif self.__is_paragraph(line):
				self.paragraphs.append(line)
			else:
				raise Exception(f"Couldn't parse line: {line}")
			

	def __regex_detect(self, pattern, tested : str) -> bool:
		"""
			Checks if a string matches a regex pattern
			args:
				pattern (str) : regex pattern
				tested (str) : string to test
			returns:
				(bool) : True if the string matches the pattern
		"""
		import re
		if re.match(pattern, tested, flags=re.I | re.M):
			return True
		return False

	def __is_olist(self, line : str):
		return self.__regex_detect(r'^[0-9]\. ', line)
	
	def __is_ulist(self, line : str):
		return self.__regex_detect(r'^- ', line)

	def __is_sublist(self, line : str):
		return self.__regex_detect(r'\t[0-9]\. ', line)

	def __is_image(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex_detect(r'!\[.*\]\(.*\)', line)

	def __is_link(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex_detect(r'\[.*\]\(.*\)', line)

	def __is_code(self, line : str):
		return self.__regex_detect(r"^`{3}.{0,}", line)

	def __is_title(self, line : str):
		return self.__regex_detect(r'^#+', line)

	def __is_paragraph(self, line : str):
		return True
	
	def __is_end_of_list(self, line : str):
		return self.__regex_detect(r'^\[END\]', line)
