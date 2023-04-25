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
    # ? Idea : Parse the content differently to pick a layout in markdown
    NOMAIN = 0
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    NOT_IMPLEMENTED = 4


class Layout:

    def __init__(self, slide: Slide, size: tuple):
        """
                This class is used to select the layout for each slide
                args:
                        slide (Slide) : slide to select the layout
                        size (tuple) : size of the pdf page (width, height)
        """
        self.slide = slide
        self.size = size
        self.coords = {}

        # These are the types considered as main items
        self.types_main_content = [
            "images", "paragraphs", "olists", "ulists", "codes"]

        self.coords = self.__get_layout(self.slide, self.coords, self.size)

        print(f"{self.coords = }")

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

        if mains > 2:
            layout = SlideLayout.NOT_IMPLEMENTED
        else:
            layout = SlideLayout(mains)

        # Note : The order of theses checks will be repercuted in the order
        # they are displayed in the pdf
        main_items_types = []
        print(f"{self.types_main_content = }")
        for item_type in self.types_main_content:
            nb_item = len(slide.items[item_type])
            if nb_item > 0:
                main_items_types.extend([item_type] * nb_item)
        print(f"THIS ONE : {main_items_types = }")
        return layout, main_items_types

    def __get_layout(self, slide: Slide, coords: dict, size: tuple) -> dict:
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
        # TODO : Wtf, make that a list or dict of functions or something
        if layout == SlideLayout.NOMAIN:
            coords = self.__nomain_layout(slide, size, coords, types)
        elif layout == SlideLayout.SINGLE:
            coords = self.__single_layout(slide, size, coords, types)
        elif layout == SlideLayout.DOUBLE:
            coords = self.__double_layout(slide, size, coords, types)
        elif layout == SlideLayout.TRIPLE:
            coords = self.__triple_layout(slide, size, coords, types)
        else:
            coords = self.__not_implemented_layout(slide)

        return coords

    def __nomain_layout(self, slide: Slide, size: tuple, coords: dict, types: list) -> dict:
        """
                This will return the coordinates of every items
                for a slide with no main content
                The title will be centered on the page, and the more titles there are
                the more they will spread up and down

                args:
                        slide (Slide) : slide to process
                        size (tuple) : size of the pdf page (width, height)
                        coords (dict) : coordinates of each item in the slide
                        types (list[str]) : list of the types of main items
                returns:
                        coords (dict) : {"Titles" : [(centered coordinates x, y + max width, max height), ]}

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

    def __single_layout(self, slide: Slide, size: tuple, coords: dict, types: list) -> dict:
        """
                This will return the coordinates of every items
                for a slide with a single main content

                args:
                        slide (Slide) : slide to process
                        size (tuple) : size of the pdf page (width, height)
                        coords (dict) : coordinates of each item in the slide
                        types (list[str]) : list of the types of main items 
                returns:
                        coords (dict) : {"Titles" : [(centered coordinates x, y + max width, max height)],
                                         "types[0]" : [(centered coordinates x, y + max width, max height)]}
        """
        # TODO : %s ? or something better than hard coded values
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
            _, s = slide.configs.get_font_size(t)
            place_titles += s

        # Compute the rest to be 100% - place_titles
        max_main_size = (self.size[1] - place_titles)
        print(f"{max_main_size = }")

        if len(slide.items["titles"]) > max_titles:
            print("WARNING : Too many titles, will only render the first 5")

        cx = self.size[0] / 2  # Centered x

        # ---------- Titles ----------
        list_coords_titles = []  # [(x, y, mw, mh), (x, y, mw, mh)]
        y_offset = top_margin
        for title in titles:
            _, s = slide.configs.get_font_size(title)
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

    def __double_layout(self, slide: Slide, size: tuple, coords: dict, types: list) -> dict:
        """
                This will return the coordinates of every items
                for a slide with a two main content
                args:
                        slide (Slide) : slide to process
                        size (tuple) : size of the pdf page (width, height)
                        coords (dict) : coordinates of each item in the slide
                        types (list[str]) : list of the types of main items
                returns:
                        coords (dict) : {"Titles" : [(centered coordinates x, y + max width, max height)],
                                         "types[0]" : [(centered coordinates x, y + max width, max height)]
                                         "types[1]" : [(centered coordinates x, y + max width, max height)]}
        """
        # TODO : %s ? or something better than hard coded values
        max_titles = 5  # ? HARD CODED : Max number of titles
        top_margin = 50  # ? HARD CODED : Margin at the top of the page
        bot_margin = 100  # ? HARD CODED : Margin at the bot of the page
        side_margin = 400  # ? HARD CODED : Margin Sides
        # ? HARD CODED : Margin between title(s) and main content
        title_main_margin = 50
        inter_title = 10  # ? HARD CODED : Interline between titles

        titles = slide.items["titles"][:max_titles]
        nb_titles = len(titles)
        print(f"{slide.items = }")
        place_titles = top_margin + inter_title * nb_titles + title_main_margin
        for t in titles:
            _, s = slide.configs.get_font_size(t)
            place_titles += s

        # Compute the rest to be 100% - place_titles
        max_main_size = (self.size[1] - place_titles)
        print(f"{max_main_size = }")

        if len(slide.items["titles"]) > max_titles:
            print("WARNING : Too many titles, will only render the first 5")

        # TODO : Make this a formula
        mainx = self.size[0] - side_margin * 2
        cxs = [side_margin + mainx / 4 -
               (side_margin // 2), side_margin + mainx * 3 / 4 + (side_margin // 2)]
        print(f"{cxs =  }")
        cx = self.size[0] / 2  # Centered x

        # ---------- Titles ----------
        list_coords_titles = []  # [(x, y, mw, mh), (x, y, mw, mh)]
        y_offset = top_margin
        for title in titles:
            _, s = slide.configs.get_font_size(title)
            y_offset += s + inter_title
            list_coords_titles.append(
                (cx, y_offset, self.size[0] - side_margin, s))

        coords["titles"] = list_coords_titles

        # ---------- Main item ----------
        # Giving centered x and y
        cy = place_titles + max_main_size / 2  # center y
        print(f"{types = }")
        for i, type in enumerate(types):
            print(f" {i = } : {type = }")
            # setdefault for creating empty list when first time seeing the type
            coords.setdefault(type, []).append(
                (cxs[i], cy, mainx // 2, max_main_size - bot_margin))

        # ---------- Links ----------
        # TODO : Add the links at the bottom

        return coords
