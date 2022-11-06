def substr_between(text : str, l : str, r : str) -> str:
	return text[text.index(l)+len(l):text.index(r)]

class slide_parser:

	def __init__(self, slide : str):
		self.slide = slide

		# Block flags
		self.f_code = False
		self.f_ulist = False
		self.f_olist = False

		self.list_is_f = [ 
			self.__is_sublist, 
			self.__is_image, 
			self.__is_link, 
			self.__is_code,
			self.__is_title,
			self.__is_olist, 
			self.__is_ulist, 
			self.__is_paragraph,
		]

		self.list_to_f = [
			self.__to_sublist, 
			self.__to_image, 
			self.__to_link, 
			self.__to_code,
			self.__to_title,
			self.__to_list, 
			self.__to_list, 
			self.__to_paragraph,
		]

		self.html = self.__parse_slide(self.slide)

	def __parse_slide(self, slide : list) -> str:
		buff = ""
		# Need to walk into the slide
		for line in self.slide:
			#print(f"{line = }")
			if not self.f_code and not self.f_olist and not self.f_ulist: # Only check if not already in block
				for i, func_is in enumerate(self.list_is_f):
					#print(f"{i = } - {func_is(line) = }")
					if func_is(line): # detected type
						# Code are blocks
						if func_is == self.__is_code:
							buff += "<pre><code data-line-numbers data-trim data-noescape>\n"
							self.f_code = not self.f_code

						# Ordered Lists are blocks
						elif func_is == self.__is_olist:
							self.f_olist = not self.f_olist
							buff += f"<ol>\n{self.__to_list(line)}"

						# Unordered Lists are blocks
						elif func_is == self.__is_ulist:
							self.f_ulist = not self.f_ulist
							buff += f"<ul>\n{self.__to_list(line)}"

						else:
							# Other (non block) inline type
							buff += self.list_to_f[i](line)
						break

			else: # In a block

				# ! END OF BLOCK CODE ?
				if self.__is_code(line):
					buff += "</code></pre>\n"
					self.f_code = not self.f_code

				# ! NOT FINDING LIST ITEM ANYMORE ?
				# ! ITS THE END OF THE LIST
				elif self.__is_end_of_list(line):  # End of list
					if self.f_olist:
						buff += "</ol>\n"
						self.f_olist = not self.f_olist
					elif self.f_ulist:
						buff += "</ul>\n"
						self.f_ulist = not self.f_ulist

				# ! STILL SOME CODE
				elif self.f_code: # Code line
					buff += self.__to_code(line)

				# ! STILL SOME LIST ITEMS
				elif self.f_olist or self.f_ulist: # List element
					buff += self.__to_list(line)

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
		return self.__regex(r'^- ', line)

	def __is_sublist(self, line : str):
		return self.__regex(r'\t[0-9]\. ', line)

	def __is_image(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex(r'!\[.*\]\(.*\)', line)

	def __is_link(self, line : str):
		# True if it matches the chars in join in order
		return self.__regex(r'\[.*\]\(.*\)', line)

	def __is_code(self, line : str):
		return self.__regex(r"^`{3}.{0,}", line)

	def __is_title(self, line : str):
		return self.__regex(r'^#+', line)

	def __is_paragraph(self, line : str):
		return True
	
	def __is_end_of_list(self, line : str):
		return self.__regex(r'^\[END\]', line)

	# INTO ENTITY

	def __to_list(self, line : str):
		# Same for ordered and unordered
		return f"\t<li>{line[2:]}</li>\n"

	def __to_title(self, line : str):
		c = line.count("#")
		return f"<h{c}>{line[c+1:]}</h{c}>\n"

	def __to_sublist(self, line : str):
		return f"\t\t<li>{line}</li>\n"

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
		return f"{line}\n"