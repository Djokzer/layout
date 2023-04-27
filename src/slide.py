import re
from config import Config
from typing import List, Tuple, Dict


class Slide:

    def __init__(self, 
				 slide: str, 
				 configs: Config) -> None:
        # ? PUT THAT INT DICT ?
        self.slide = slide
        self.configs = configs
        self.items = {
            "titles": [],  # str[]
            "paragraphs": [],  # str[]
            "olists": [],  # str[[str]]
            "ulists": [],  # str[[str]]
            "images": [],  # str[]
            "links": [],  # str[]
            "codes": []  # str[]
        }
        self.parse(slide)

    def parse(self, 
              slide: str):
        """
                Parse a slide and fill the attributes
                args:
                        slide (str) : 
                        	slide to parse
        """

        slide, self.items["codes"] = self.extract_code_blocks(slide)
        slide, self.items["olists"] = self.extract_olists(slide)
        slide, self.items["ulists"] = self.extract_ulists(slide)

        # Split the slide into lines and remove empty lines
        lines = list(filter(None, slide.split("\n")))

        for line in lines:
            if self.__is_title(line):
                self.items["titles"].append(line)
            elif self.__is_image(line):
                self.items["images"].append(line)
            elif self.__is_link(line):
                self.items["links"].append(line)
            elif self.__is_paragraph(line):
                self.items["paragraphs"].append(line)
            else:
                raise Exception(f"Couldn't parse line: {line}")

    def __regex_detect(self, 
					   pattern, 
					   tested: str) -> bool:
        """
                Checks if a string matches a regex pattern
                args:
                        pattern (str) : 
							regex pattern
                        tested (str) : 
							string to test
                returns (bool):
                    True if the string matches the pattern
        """

        if re.match(pattern, tested, flags=re.I | re.M):
            return True
        return False

    # TODO : REFACTOR THESE 3 ONES INTO ONE
    def extract_code_blocks(self, 
                            slide: str) -> Tuple[str, List[str]]:
        """
        Extracts the code blocks from a slide
        args:
			slide (str) : 
            	slide to parse
        
        returns (Tuple[str, List[str]]) :
			(str) : slide without code blocks, 
			(List[str]) : list of code blocks
        """

        pattern = re.compile(r"(```[\w+]*)\n(.*?)\n(```)", re.DOTALL)

        # Find and extract the code blocks
        code_blocks = pattern.findall(slide)
        codes = [f"{block[0]}\n{block[1]}\n{block[2]}" for block in code_blocks]
        out_slide = pattern.sub('', slide)
        return out_slide, codes

    def extract_olists(self, 
                       slide: str) -> Tuple[str, List[List[str]]]:
        """
        Extracts the ordered lists from a slide
        args:
			slide (str) : slide to parse
        returns (Tuple[str, List[List[str]]]):
			(str) : slide without ordered lists
			(list[list[str]]) : list of ordered lists
        """
        olists = []

        # regex pattern to match an ordered list element
        pattern = re.compile(r'([0-9]+\. .*)')

        current_list = []
        for line in slide.split("\n"):
            if pattern.match(line):
                current_list.append(line)
            else:
                if current_list:
                    olists.append(current_list)
                    current_list = []
        if current_list:
            olists.append(current_list)
        out_slide = pattern.sub('', slide)

        return out_slide, olists

    def extract_ulists(self, 
                       slide: str) -> Tuple[str, List[List[str]]]:
        """
        Extracts the unordered lists from a slide
        args:
			slide (str) : 
            	slide to parse
        returns (Tuple[str, List[List[str]]]):
			(str) : 
            	slide without unordered lists
			(List[List[str]]) : 
            	list of unordered lists
        """
        ulists = []

        # regex pattern to match an unordered list element
        pattern = re.compile(r'(- .*)')

        current_list = []
        for line in slide.split("\n"):
            if pattern.match(line):
                current_list.append(line)
            else:
                if current_list:
                    ulists.append(current_list)
                    current_list = []
        if current_list:
            ulists.append(current_list)
        out_slide = pattern.sub('', slide)

        return out_slide, ulists

    def __is_image(self, 
                   line: str):
        # True if it matches the chars in join in order
        return self.__regex_detect(r'!\[.*\]\(.*\)', line)

    def __is_link(self, 
                  line: str):
        # True if it matches the chars in join in order
        return self.__regex_detect(r'\[.*\]\(.*\)', line)

    def __is_title(self, 
                   line: str):
        return self.__regex_detect(r'^#+', line)

    def __is_paragraph(self, 
                       line: str):
        return self.__regex_detect(r'.*', line)
