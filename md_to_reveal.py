def substr_between(text : str, l : str, r : str) -> str:
	return text[text.index(l)+len(l):text.index(r)]




class slide_parser:

	def __init__(self, line : str):
		
		self.line = line
		self.func = self.__detect(self.line)

	def __detect(self, line):
		"""
			Returns the function to apply to the detected md

			Args:
				line : str - The line to check
		"""
		if self.__is_list(self.line):
			return self.__to_list
		if self.__is_sublist(self.line):
			return self.__to_sublist
		elif self.__is_image(self.line):
			return self.__to_image
		elif self.__is_link(self.line):
			return self.__to_link
		elif self.__is_code(self.line):
			return self.__to_code
		elif self.__is_title(self.line):
			return self.__to_title
		else:
			return self.__to_paragraph(self.line)


	def __r(self, pattern, tested : str):
		import re
		if re.match(pattern, tested, flags=re.I | re.M):
			return True
		return False

	# IS ENTITY
	def __is_list(self, line : str):
		return self.__r(r'^[0-9]\. ', line) or self.__r("^- ", line)

	def __is_sublist(self, line : str):
		return self.__r(r'\t[0-9]\. ', line)

	def __is_image(self, line : str):
		# True if it matches the chars in join in order
		return self.__r(r'!\[.*\]\(.*\)', line)

	def __is_link(self, line : str):
		# True if it matches the chars in join in order
		return self.__r(r'\[.*\]\(.*\)', line)

	def __is_code(self, line : str):
		return self.__r(r"^`{3}\n", line)

	def __is_title(self, line : str):
		return self.__r("#+", line)

	# INTO ENTITY
	def __to_list(self, ):
		print(f"To List")

	def __to_title(self, ):
		print(f"To title")

	def __to_sublist(self, ):
		print(f"To sublist")

	def __to_image(self, ):
		print(f"To image")

	def __to_link(self, ):
		print(f"To link")
	
	def __to_paragraph(self, ):
		print(f"To Paragraph")
	
	def __to_code(self, ):
		print(f"To code")