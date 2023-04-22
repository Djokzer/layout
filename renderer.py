# Author: Jonas S.
# Date : 22/04/2023
# Renderer : This class is used to render the slides. It takes slides
# and configs as input and renders the slides into a pdf file.
# It will select a layout for each slide based on the number of items

from slides import Slides 
from config import Config
from slide import Slide
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class Renderer:

	def __init__(self, slides : Slides, size : tuple):
		self.slides = slides
		self.configs, self.slides = self.slides.get()
		self.size = size
		self.font_name = ""

		self.pdf = canvas.Canvas("output.pdf", pagesize=self.size, bottomup=False)
		self.__pdf_setup(self.pdf, self.configs)

		# Adding titles
		self.__add_titles(self.pdf, self.slides[0])
		self.pdf.drawCentredString(100, 200, "HELO")
		self.__pdf_finish_page(self.pdf)

		self.__add_titles(self.pdf, self.slides[1])
		self.pdf.drawCentredString(100, 200, "HELO")
		self.__pdf_finish_page(self.pdf)

		self.__pdf_save(self.pdf)

	def __pdf_setup(self, pdf : canvas.Canvas, configs : Config):
		self.pdf.setAuthor(self.configs.settings["author"])
		self.pdf.setTitle(self.configs.settings["title"])
		self.pdf.setSubject(self.configs.settings["date"])

		self.font_name = self.configs.settings["font"].split("/")[-1].split(".")[0]
		print(self.font_name)
		pdfmetrics.registerFont(TTFont(self.font_name, configs.settings["font"]))
		self.pdf.setFont(self.font_name, 20)

	def __pdf_finish_page(self, pdf : canvas.Canvas):
		self.pdf.showPage()

	def __pdf_save(self, pdf : canvas.Canvas):
		self.pdf.save()

	#def render(self, ):


	def __add_titles(self, pdf : canvas.Canvas, slide : Slide, ):
		"""
			This adds the titles to the slide
			args:
				slide (Slide) : Slide containing the titles
				pdf (canvas.Canvas) : pdf to add the titles to
			returns:
				None
		"""
		center_x = self.size[0] // 2
		self.__draw_title(pdf, slide.titles[0], center_x, 100)

	def __draw_title(self, pdf : canvas.Canvas, title : str, x : int, y : int):
		"""
			This sets the font size accroding to the depth of the title
			and draws the title and resets the font size 
		"""
		default = pdf._fontsize
		# One '#' is the biggest title '#####' is the smallest
		parts = title.split(' ', 1)
		hashes = parts[0]
		title = parts[1]

		pdf.setFont(self.font_name, 42 - (len(hashes) * 2))
		pdf.drawCentredString(x, y, title)
		pdf.setFont(self.font_name, default)