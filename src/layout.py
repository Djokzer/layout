# Author: Jonas S.
# Date : 22/04/2023
# Layout : This class is used to select the layout
# for each slide based on the number of items
# It will give coordinates for each item in the slide

from enum import Enum
from slide import Slide
from typing import List, Tuple, Dict



class SlideLayout(Enum):
	# ENUM FOR LAYOUTS
	# The layout is based on the number of main items in the slide
	# Main items are images, texts, lists or codes
	NOMAIN = 0
	MULTIPLE = 1
	NOT_IMPLEMENTED = 2

class Layout:

	def __init__(self, slide: Slide, size: Tuple[int, int]):
		"""
				This class is used to select the layout for each slide
				args:
						slide (Slide) : slide to select the layout
						size (Tuple[int, int]) : size of the pdf page (width, height)
		"""
		self.slide = slide
		self.size = size
		self.coords = {}

		# Map the layout to the layout function
		self.layouters = { 	SlideLayout.NOMAIN : self.__nomain_layout,
							SlideLayout.MULTIPLE : self.__horizontal_layout,
		}
		
		# These are the types considered as main items
		self.types_main_content = [
			"images", "paragraphs", "olists", "ulists", "codes"]

		self.coords = self.__get_layout(self.slide, self.coords, self.size)



	def get_coords(self):
		return self.coords

	def select(self, slide: Slide) -> tuple:
		"""
				This gives us the layout for the slide and the types of main 
				items
				args:
					None
				returns:
					layout (SlideLayout) : layout of the slide
					items_types (list[str]) : list of the types of main items
		"""
		# Count the number of main items
		mains = len(slide.items["images"]) + len(slide.items["paragraphs"]) + len(
			slide.items["olists"]) + len(slide.items["ulists"]) + len(slide.items["codes"])

		if mains > 0:
			layout = SlideLayout.MULTIPLE
		else:
			layout = SlideLayout.NOMAIN

		# Note : The order of theses checks will be repercuted in the order
		# they are displayed in the pdf
		main_items_types = []
		for item_type in self.types_main_content:
			nb_item = len(slide.items[item_type])
			if nb_item > 0:
				main_items_types.extend([item_type] * nb_item)
		return layout, main_items_types

	def __get_layout(	self, 
		  				slide: Slide, 
		  				coords: Dict[str, List[ Tuple[int, int] ]], 
						size: Tuple[int, int]) -> Dict[str, List[ Tuple[int, int] ]]:
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
						slide (Slide) : 
							slide to process
						coords (Dict[str, List[ Tuple[int, int] ]]) : 
							Base dictionary to fill
						size (Tuple[int, int]) : 
							size of the pdf page (width, height)
				returns:
						coords (Dict[str, List[ Tuple[int, int] ]]) : 
							coordinates of each item in the slide
		"""

		layout, types = self.select(self.slide)
		if(layout == SlideLayout.NOMAIN):
			coords = self.layouters[layout](slide, size, coords, types)
		else:
			coords = self.layouters[layout](slide, size, None, types)
		
		return coords


	def __nomain_layout(self, 
		     			slide: Slide, 
						size: Tuple[int, int], 
						coords: Dict[str, List[ Tuple[int, int] ]], 
						types: List[str]) -> Dict[str, List[ Tuple[int, int] ]]:
		"""
				This will return the coordinates of every items
				for a slide with no main content
				The title will be centered on the page, and the more titles there are
				the more they will spread up and down

				args:
						slide (Slide) : 
							slide to process
						size (Tuple[int, int]) : 
							size of the pdf page (width, height)
						coords (Dict[str, List[ Tuple[int, int] ]]) : 
							coordinates of each item in the slide
						types (List[str]) : 
							list of the types of main items
				returns:
						coords (dict) : 
							{"Titles" : [(centered coordinates x, y + max width, max height), ]}

		"""
		# There should only be titles there
		horizontal_margin = 100  # Left and Right
		max_titles = 5 			# ? HARD CODED : Max number of titles
		titles = slide.items["titles"][:max_titles]
		nb_titles = len(titles)

		cx = (size[0] - horizontal_margin) / 2 + (horizontal_margin / 2)

		def get_title_y_coordinates(num_titles):
			delta_y = size[1] / (num_titles + 1)
			return [delta_y * (i + 1) for i in range(num_titles)]

		list_coords_titles = []  # [(x, y), (x, y)]
		for i in range(nb_titles):
			# Center titles on each chunky
			list_coords_titles.append(
				(cx, get_title_y_coordinates(nb_titles)[i]))

		coords["titles"] = list_coords_titles

		return coords

	def __single_layout(self, 
		     			slide: Slide, 
						size: Tuple[int, int], 
						coords: Dict[str, List[ Tuple[int, int] ]], 
						types: list[str]) -> Dict[str, List[ Tuple[int, int] ]]:
		"""
				This will return the coordinates of every items
				for a slide with a single main content

				args:
						slide (Slide) : 
							slide to process
						size (Tuple[int, int]) : 
							size of the pdf page (width, height)
						coords (Dict[str, List[ Tuple[int, int] ]]) : 
							coordinates of each item in the slide
						types (list[str]) : 
							list of the types of main items 
				returns:
						coords (Dict[str, List[ Tuple[int, int] ]]) : 
						{
							"Titles" : [(centered coordinates x, y + max width, max height)],
							"types[0]" : [(centered coordinates x, y + max width, max height)]
						}
		"""
		# TODO : % or something better than hard coded values
		max_titles = 5  # ? HARD CODED : Max number of titles
		top_margin = 50  # ? HARD CODED : Margin at the top of the page
		bot_margin = 100  # ? HARD CODED : Margin at the bot of the page
		side_margin = 400  # ? HARD CODED : Margin Sides
		# ? HARD CODED : Margin between title(s) and main content
		title_main_margin = 50
		inter_title = 10  # ? HARD CODED : Interline between titles

		titles = slide.items["titles"][:max_titles]
		nb_titles = len(titles)

		place_titles = top_margin + inter_title * nb_titles + title_main_margin
		for t in titles:
			_, s = slide.configs.get_title_font_size(t)
			place_titles += s

		# Compute the rest to be 100% - place_titles
		max_main_size = (self.size[1] - place_titles)

		if len(slide.items["titles"]) > max_titles:
			print("WARNING : Too many titles, will only render the first 5")

		cx = self.size[0] / 2  # Centered x

		# ---------- Titles ----------
		list_coords_titles = []  # [(x, y, mw, mh), (x, y, mw, mh)]
		y_offset = top_margin
		for title in titles:
			_, s = slide.configs.get_title_font_size(title)
			y_offset += s + inter_title
			list_coords_titles.append(
				(cx, y_offset, self.size[0] - side_margin, s))

		coords["titles"] = list_coords_titles

		# ---------- Main item ----------
		# Giving centered x and y
		list_coords_items = []  # [(x, y, mw, mh), (x, y, mw, mh)]
		cy = place_titles + max_main_size / 2  # center y
		list_coords_items.append(
			(cx, cy, self.size[0] - side_margin, max_main_size - bot_margin))

		coords[types[0]] = list_coords_items

		# ---------- Links ----------
		# TODO : Add the links at the bottom

		return coords

	def __double_layout(self, slide: Slide, size: Tuple[int, int], coords: Dict[str, List[ Tuple[int, int] ]], types: list) -> Dict[str, List[ Tuple[int, int] ]]:
		"""
				This will return the coordinates of every items
				for a slide with a two main content
				args:
						slide (Slide) : slide to process
						size (Tuple[int, int]) : size of the pdf page (width, height)
						coords (Dict[str, List[ Tuple[int, int] ]]) : coordinates of each item in the slide
						types (list[str]) : list of the types of main items
				returns:
						coords (Dict[str, List[ Tuple[int, int] ]]) : {"Titles" : [(centered coordinates x, y + max width, max height)],
										 "types[0]" : [(centered coordinates x, y + max width, max height)]
										 "types[1]" : [(centered coordinates x, y + max width, max height)]}
		"""
		# TODO : %s ? or something better than hard coded values
		max_titles = 5  # ? HARD CODED : Max number of titles
		top_margin = 50  # ? HARD CODED : Margin at the top of the page
		bot_margin = 100  # ? HARD CODED : Margin at the bot of the page
		side_margin = 100  # ? HARD CODED : Margin Sides
		# ? HARD CODED : Margin between title(s) and main content
		title_main_margin = 50
		inter_title = 10  # ? HARD CODED : Interline between titles

		titles = slide.items["titles"][:max_titles]
		nb_titles = len(titles)
		place_titles = top_margin + inter_title * nb_titles + title_main_margin
		for t in titles:
			_, s = slide.configs.get_title_font_size(t)
			place_titles += s

		# Compute the rest to be 100% - place_titles
		max_main_size = (self.size[1] - place_titles)

		if len(slide.items["titles"]) > max_titles:
			print("WARNING : Too many titles, will only render the first 5")

		# TODO : Make this a formula
		mainx = self.size[0] - side_margin * 2
		cxs = [side_margin + mainx / 4 -
			   (side_margin // 2), side_margin + mainx * 3 / 4 + (side_margin // 2)]
		cx = self.size[0] / 2  # Centered x

		# ---------- Titles ----------
		list_coords_titles = []  # [(x, y, mw, mh), (x, y, mw, mh)]
		y_offset = top_margin
		for title in titles:
			_, s = slide.configs.get_title_font_size(title)
			y_offset += s + inter_title
			list_coords_titles.append(
				(cx, y_offset, self.size[0] - side_margin, s))

		coords["titles"] = list_coords_titles

		# ---------- Main item ----------
		# Giving centered x and y
		cy = place_titles + max_main_size / 2  # center y
		for i, type in enumerate(types):
			# setdefault for creating empty list when first time seeing the type
			coords.setdefault(type, []).append(
				(cxs[i], cy, mainx // 2, max_main_size - bot_margin))

		# ---------- Links ----------
		# TODO : Add the links at the bottom

		return coords

	def __horizontal_layout(self, 
			 				slide: Slide, 
							size: Tuple[int, int],
							params: List[str],
							types: List[str]) -> Dict[str, List[ Tuple[int, int, int, int] ]]:
		"""
		This will return the coordinates of every items
		for a slide with single or multiple main content,
		in a horizontal layout

		args:
				slide (Slide) : 
					slide to process
				size (Tuple[int, int]) : 
					size of the pdf page (width, height)
				params (List[str]):
					List of scale for each main items
				types (List[str]) : 
					list of the types of main items
		returns:
				coords (dict) : 
					{"Titles" : [(centered coordinates x, y + max width, max height), ]}

		"""
		max_titles = 5  # ? HARD CODED : Max number of titles
		top_margin = 50  # ? HARD CODED : Margin at the top of the page
		bot_margin = 100  # ? HARD CODED : Margin at the bot of the page
		side_margin = 100  # ? HARD CODED : Margin Sides
		# ? HARD CODED : Margin between title(s) and main content
		title_main_margin = 50
		inter_title = 10  # ? HARD CODED : Interline between titles
		max_main_item = 5 # ? HARD CODED : Max number of main items
		inter_margin = 30 # ? HARD CODED : Margin between main items
		
		coords = {}	# CORDINATES DICT

		titles = slide.items["titles"][:max_titles]
		nb_titles = len(titles)
		place_titles = top_margin + inter_title * nb_titles + title_main_margin
		for t in titles:
			_, s = slide.configs.get_title_font_size(t)
			place_titles += s

		# Compute the rest to be 100% - place_titles
		max_main_size = (self.size[1] - place_titles)

		if len(slide.items["titles"]) > max_titles:
			print("WARNING : Too many titles, will only render the first 5")

		# ---------- Titles ----------
		list_coords_titles = []  # [(x, y, mw, mh), (x, y, mw, mh)]
		cx = self.size[0] / 2  	# Centered x
		y_offset = top_margin
		for title in titles:
			_, s = slide.configs.get_title_font_size(title)
			y_offset += s + inter_title
			list_coords_titles.append(
				(cx, y_offset, self.size[0] - side_margin, s))

		coords["titles"] = list_coords_titles

		# KEEP ONLY MAIN ITEMS UNDER MAX
		types = types[:max_main_item]

		# TODO : Take params for scale
		mainx = self.size[0] - side_margin * 2
		mainy = max_main_size - bot_margin
		item_width = mainx // len(types)
		item_height = mainy
		first_item_cx = side_margin + (item_width // 2)

		#cxs = [side_margin + mainx / 4 -
		#	   (side_margin // 2), side_margin + mainx * 3 / 4 + (side_margin // 2)]
		
		# ---------- Main item ----------
		# Giving centered x and y
		cy = place_titles + max_main_size / 2  # center y
		for i, type in enumerate(types):
			# setdefault for creating empty list when first time seeing the type
			coords.setdefault(type, []).append(
				(first_item_cx + (i * item_width), cy, item_width - inter_margin, item_height - inter_margin))

		return coords