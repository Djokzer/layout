# Author: Jonas S.
# Date : 22/04/2023
# Layout : This class is used to select the layout
# for each slide based on the number of items
# It will give coordinates for each item in the slide

from enum import Enum
from slide import Slide


class SlideLayout(Enum):
	# ENUM FOR LAYOUTS
	# The layout is based on the number of main items in the slide
	# Main items are images, texts, lists or codes
	# No main content (0 ain items)
	# Single content  (1 main items)
	# Double contents (2 main items)
	# Triple contents (3 main items)
	# NOT IMPLEMENTED FOR NOW 
	# ? Idea : Titled content (sub titles are for the main items)
	NOMAIN = 0
	SINGLE = 1
	DOUBLE = 2
	TRIPLE = 3 
	NOT_IMPLEMENTED = 4
    
class Layout:
    
	def __init__(self, slide : Slide, size : tuple):
		"""
			This class is used to select the layout for each slide
			args:
				slide (Slide) : slide to select the layout
				size (tuple) : size of the pdf page (width, height)
		"""
		self.slide = slide
		self.size = size
		self.coords = {}
		self.coords = self.__get_layout(self.slide, self.coords, self.size)

		print(f"{self.coords = }")

	def get_cords(self):
		return self.coords

	def select(self, slide : Slide) -> tuple:
		"""
			This gives us the layout for the slide and the types of main items
			args:
				None
			returns:
				layout (SlideLayout) : layout of the slide
				items_types (list[str]) : list of the types of main items
		"""
		# Count the number of main items
		mains = len(slide.items["images"]) + len(slide.items["paragraphs"]) + len(slide.items["olists"]) + len(slide.items["ulists"]) + len(slide.items["codes"])

		if mains > 2:
			layout = SlideLayout.NOT_IMPLEMENTED
		else:
			layout = SlideLayout(mains)

		# Note : The order of theses checks will be repercuted in the order
		# they are displayed in the pdf
		main_items_types = []
		if len(slide.items["images"]) > 0:
			main_items_types.append("images")
		if len(slide.items["paragraphs"]) > 0:
			main_items_types.append("paragraphs")
		if len(slide.items["olists"]) > 0:
			main_items_types.append("olists")
		if len(slide.items["ulists"]) > 0:
			main_items_types.append("ulists")
		if len(slide.items["codes"]) > 0:
			main_items_types.append("codes")

		return layout, main_items_types 
	
	def __get_layout(self, slide : Slide, coords : dict, size : tuple) -> dict: 
		"""
			This will process the layout of the slides
			and return every item a coordinate
			in a dictionary 
			
			E.g.
			coords{
				"title" 	 : [(x, y), (x, y)],
				"paragraphs" : [(x, y), (x, y)],
				"olits" 	 : [(x, y), (x, y)],
				"ulits" 	 : [(x, y), (x, y)],
				...
			}

			args:
				slide (Slide) : slide to process
				coords (dict) : Base dictionary to fill
				size (tuple) : size of the pdf page (width, height)
			returns:
				coords (dict) : coordinates of each item in the slide
		"""
		
		layout, types = self.select(self.slide)
		# TODO : Wtf, make that a list of functions or something
		if layout == SlideLayout.NOMAIN:
			coords = self.__nomain_layout(slide, size, coords, types)
		if layout == SlideLayout.SINGLE:
			coords = self.__single_layout(slide, size, coords, types)
		elif layout == SlideLayout.DOUBLE:
			coords = self.__double_layout(slide, size, coords, types)
		elif layout == SlideLayout.TRIPLE:
			coords = self.__triple_layout(slide, size, coords, types)
		else:
			coords = self.__not_implemented_layout(slide)

		return coords
	
	def __nomain_layout(self, slide : Slide, size : tuple, coord : dict, types : list):
		"""
			This will return the coordinates of every items
			for a slide with no main content
		"""
		pass
	


	def __single_layout(self, slide : Slide, size : tuple, coords : dict, types : list) -> dict:
		"""
			This will return the coordinates of every items
			for a single layout

			args:
				slide (Slide) : slide to process
				size (tuple) : size of the pdf page (width, height)
				coords (dict) : coordinates of each item in the slide
				types (list[str]) : list of the types of main items 
			returns:
				coords (dict) : coordinates of each item in the slide
		"""
		max_titles = 5 # ? HARD CODED : Max number of titles
		max_title_size = 1 / 3 # 30% of the slide

		# Compute the rest to be 100% - max_title_size
		max_main_size = 1 - max_title_size

		if len(slide.items["titles"]) > max_titles:
			print("WARNING : Too many titles, will only render the first 5")

		cx = self.size[0] / 2

		# ---------- Titles ----------
		# TODO : Chose these values according to the font size
		# For now its just the 30% / number of titles
		chunk_y_titles = int(self.size[1] * max_title_size) / len(slide.items["titles"][:max_titles])

		list_coords_titles = [] # [(x, y), (x, y)]
		for i, title in enumerate(slide.items["titles"][:max_titles]):
			y = chunk_y_titles * i + chunk_y_titles / 2
			list_coords_titles.append((cx, y))

		coords["titles"] = list_coords_titles

		# ---------- Main item ----------
		# Giving centered x and y
		list_coords_items = [] # [(x, y), (x, y)]
		size_y_main = int(self.size[1] * max_main_size) # remaining space for the main item
		cy = self.size[1] / 2 + size_y_main / 2 # center y
		list_coords_items.append((cx, cy))

		coords[types[0]] = list_coords_items

		# ---------- Links ----------
		# Add the links at the bottom

		return coords


#self.titles 	= [] # str[]
#self.paragraphs = [] # str[]
#self.olists 	= [] # str[[str]]
#self.ulists 	= [] # str[[str]]
#self.images 	= [] # str[]
#self.codes 		= [] # str[]
#self.links 		= [] # str[]