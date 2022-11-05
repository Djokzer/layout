def substr_between(text : str, l : str, r : str) -> str:
	return text[text.index(l)+len(l):text.index(r)]

class slide_parser:

	def __init__(self, slide : str):
		self.slide = slide

		self.list_is_f = [ 
			self.__is_olist, 
			self.__is_ulist, 
			self.__is_sublist, 
			self.__is_image, 
			self.__is_link, 
			self.__is_code,
			self.__is_title,
			self.__is_paragraph,
		]

		self.list_to_f = [
			self.__to_olist, 
			self.__to_ulist, 
			self.__to_sublist, 
			self.__to_image, 
			self.__to_link, 
			self.__to_code,
			self.__to_title,
			self.__to_paragraph,
		]

		self.f_code = False
		self.f_list = False

		self.html = self.__parse_slide(self.slide)

	def __parse_slide(self, slide : list) -> str:
		buff = ""
		# Need to walk into the slide
		for line in self.slide:
			#print(f"{line = }")
			if not self.f_code and not self.f_list: # Only check if not already in block
				for i, func_is in enumerate(self.list_is_f):
					#print(f"{func_is(line) = }")
					#print(f"{i = }")
					if func_is(line): # detected type
						# Code are blocks
						if func_is == self.__is_code:
							buff += "<pre><code>\n"
							self.f_code = not self.f_code

						# Ordered Lists are blocks
						elif func_is == self.__is_olist:
							self.f_list = not self.f_list
							buff += "<ol>\n"

						# Unordered Lists are blocks
						elif func_is == self.__is_ulist:
							self.f_list = not self.f_list
							buff += "<ul>\n"

						else:
							# Other (non block) inline type
							buff += self.list_to_f[i](line)
							#print(f"{buff = }")
						break

			else: # In block
				if self.__is_code(line): # End of block
					buff += "<\\code><\\pre>\n"
					self.f_code = not self.f_code

				elif self.__is_olist(line) or self.__is_ulist(line): # End of list
					buff += "<\\ul>\n"
					self.f_list = not self.f_list

				elif self.f_code: # Code line
					buff += self.__to_code(line)

				elif self.f_list: # List element
					buff += self.__to_ulist(line)
		return buff


	def __regex(self, pattern, tested : str):
		import re
		if re.match(pattern, tested, flags=re.I | re.M):
			return True
		return False

	# IS ENTITY
	def __is_olist(self, line : str):
		return self.__regex(r'^[0-9]\. ', line)
	
	def __is_ulist(self, line : str):
		return self.__regex("^- ", line)

	def __is_sublist(self, line : str):
		return self.__regex(r'\t[0-9]\. ', line)

	def __is_image(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex(r'!\[.*\]\(.*\)', line)

	def __is_link(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex(r'\[.*\]\(.*\)', line)

	def __is_code(self, line : str):
		return self.__regex(r"^`{3}.+\n", line)

	def __is_title(self, line : str):
		return self.__regex('^#+', line)

	def __is_paragraph(self, line : str):
		return True


	# INTO ENTITY
	def __to_olist(self, line : str):
		return f"\t\t<li>{line}<\\li>\n"

	def __to_ulist(self, line : str):
		return f"\t\t<li>{line}<\\li>\n"

	def __to_title(self, line : str):
		c = line.count("#")
		return f"<h{c}>{line[c+1:]}</h{c}>\n"

	def __to_sublist(self, line : str):
		return f"\t\t<li>{line}<\\li>\n"

	def __to_image(self, line : str):
		link = substr_between(line, "[", "]")
		return f'<img src="{link}" width="450" height="300">\n'

	def __to_link(self, line : str):
		link = substr_between(line, "[", "]")
		text = substr_between(line, "(", ")")
		return f'<a href="{link}">{text}</a>\n'

	def __to_paragraph(self, line : str):
		return line
	
	def __to_code(self, line : str):
		return line