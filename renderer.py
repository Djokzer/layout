# Author: Jonas S.
# Date : 22/04/2023
# Renderer : This class is used to render the slides. It takes slides
# and configs as input and renders the slides into a pdf file.
# It will select a layout for each slide based on the number of items

from slides import Slides 
from config import Config
from slide import Slide
from layout import Layout

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class Renderer:

	def __init__(self, slides : Slides, size : tuple):
		"""
			This class is used to render the slides into a pdf file
			args:
				slides (Slides) : slides to render
				size (tuple) : size of the pdf page (width, height)
		"""

		self.slides = slides
		self.configs, self.slides = self.slides.get()
		self.size = size

		# FONT
		self.font_name = ""
		self.default_fontsize = 20
		
		# PDF
		self.pdf = canvas.Canvas("output.pdf", pagesize=self.size, bottomup=False)
		self.__pdf_setup(self.pdf, self.configs)
		self.current_page = 0


		# Adding titles
		#self.__draw_title(self.pdf, self.slides[0].titles[0], self.size[0] // 2, 50)
		#self.__draw_title(self.pdf, self.slides[0].titles[1], self.size[0] // 2, 100)
		#self.__draw_title(self.pdf, self.slides[0].titles[1], self.size[0] // 2, 150)
		#self.__draw_title(self.pdf, self.slides[0].titles[1], self.size[0] // 2, 200)
		#self.__draw_title(self.pdf, self.slides[0].titles[1], self.size[0] // 2, 250)
		#self.__draw_title(self.pdf, self.slides[0].titles[1], self.size[0] // 2, 300)
		# Dict of drawers, for each type of item
		self.drawers = {	"titles" : self.__draw_title,
							"paragraphs" : self.__draw_paragraph,}
		  					#"images" : self.__draw_image,
							#"olists" : self.__draw_olist,
							#"ulists" : self.__draw_ulist,
							#"codes" : self.__draw_code}

		self.__render_slide(self.slides[0])
		self.__pdf_finish_page(self.pdf)

		self.__pdf_save(self.pdf)

	def __render_slide(self, slide : Slide):
		l = Layout(slide, (self.size[0], self.size[1]))
		coords = l.get_cords()
		for key, coord in coords.items(): 	# For each available items types
			#print(f"{key = } {coord = }")
			drawer = self.drawers[key] 		# Get the drawer
			# For each item of that type
			for i, c in enumerate(coord):
				#print(f"{c = }")
				#print(f"{(c[0], c[1]) = }")
				#print(f"{slide.items[key][i] = }")
				drawer(self.pdf, slide.items[key][i], (c[0], c[1]))

			#		drawer(self.pdf, item, coord[0], coord[1]) 

	def __draw_paragraph(self, pdf : canvas.Canvas, paragraph : str, coord : tuple):
		"""
			This draws a paragraph
			args:
				pdf (canvas.Canvas) : pdf to add the paragraph to
				paragraph (str) : paragraph to draw
				coord (tuple) : coordinates of the paragraph
			returns:
				None
		"""
		pdf.drawCentredString(coord[0], coord[1], paragraph)

	def __draw_title(self, pdf : canvas.Canvas, title : str, coord : tuple):
		"""
			This sets the font size accroding to the depth of the title
			and draws the title and resets the font size 
			args:
				pdf (canvas.Canvas) : pdf to add the titles to
				title (str) : title to draw
				coord (tuple) : coordinates of the title
			returns:
				None
		"""
		default = pdf._fontsize
		# One '#' is the biggest title '#####' is the smallest
		parts = title.split(' ', 1)
		hashes = parts[0]
		title = parts[1]

		# ? This chooses the font size according to the depth of the title
		pdf.setFont(self.font_name, 102 - (len(hashes) * 20)) 
		pdf.drawCentredString(coord[0], coord[1], title)
		pdf.setFont(self.font_name, self.default_fontsize)

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
		self.current_page += 1

	def __pdf_save(self, pdf : canvas.Canvas):
		self.pdf.save()
