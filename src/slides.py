from slide import Slide
from config import Config
from typing import List, Dict, Tuple

class Slides:

	def __init__(self, 
				 filename : str):
		"""
			This class is used to parse a markdown file into slides
			args:
				filename (str) :
					filename of the markdown file
		"""
		self.filename = filename
		self.raw = self.__get_raw_md(self.filename)
		self.configs = self.__get_configs(self.raw)
		self.slides_str = self.__get_slides_str(self.raw)
		self.configs = Config(self.configs)
		self.slides = self.__parse_slides(self.slides_str)

	def get(self) -> Tuple[List[str], List[Slide]]:
		"""
			This gives us the raw markdown file, the configs and the slides
			args:
				None
			returns:
				(Tuple[List[str], List[Slide]]) : 
					configs and slides
		"""
		return self.configs, self.slides

	def __parse_slides(self, 
					   slides_str : List[str]) -> List[Slide]:
		"""
			This gives us a list of slides
			args:
				slides_str (List[str]) : 
					list of slides as string
			returns:
				slides (List[Slide]) : 
					list of slides
		"""
		slides = []
		for slide in slides_str:
			slides.append(Slide(slide, self.configs))
		return slides

	def __get_raw_md(self, 
					 filename : str) -> str:
		"""
			This gives us the raw markdown file
			args:
				filename (str) : 
					filename of the markdown file
			returns:
				raw (str) : 
					raw markdown file as a string
		"""
		import re
		md = ""
		with open(filename) as f:
			md = f.read()
		# Clean up a bit
		return re.sub(r'\n+', '\n', md)

	def __get_configs(self, 
					  md : str) -> List[str]:
		# Skip first --- and empty char
		return list(filter(None, md.split("---")[1].split("\n")))

	def __get_slides_str(self, 
						 md : str) -> List[str]:
		"""
			This gives us a list of slides
			args:
				md (str): 
					raw markdown file as a string 
			returns:
				slides (List[str]): 
					list of slides
		"""
		# get rid of the config header
		out = md.split('---', 2)[-1]
		#print(f"{out.split('---')=}")
		out = map(lambda x: x.strip(), out.split('---'))
		out = filter(None, out)

		return out