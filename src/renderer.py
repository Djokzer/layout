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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from typing import List, Tuple


class Renderer:
	def __init__(self, 
				 output_file: str,
				 slides: Slides,
				 size: Tuple[int, int]):
		"""
		This class is used to render the slides into a pdf file
		args:
			output_file (str) :
				path to the output file
			slides (Slides) : 
				slides to render
			size (tuple) : 
				size of the pdf page (width, height)
		"""

		self.slides = slides
		self.configs, self.lst_slides = self.slides.get()
		self.size = size

		# FONT
		self.default_fontsize = int(slides.configs.settings["font-size-text"])
		self.title_fontsize = int(slides.configs.settings["font-size-title"])
		self.font_name = slides.configs.settings["font"]

		# PDF
		# bottomup = False : 0,0 at top left because wtf is wrong with people
		self.pdf = canvas.Canvas(
			output_file, pagesize=self.size, bottomup=False)
		self.__pdf_setup(self.pdf, self.configs)
		self.current_page = 1

		# Dict of drawers, for each type of item
		self.drawers = {
			"titles": self.__draw_title,
			"paragraphs": self.__draw_paragraph,
			"images": self.__draw_image,
			"olists": self.__draw_olist,
			"ulists": self.__draw_ulist,
			"codes": self.__draw_code}

		self.__render_slides(self.pdf, self.lst_slides)

		self.__pdf_save(self.pdf)

	def __render_slides(self, 
						pdf: canvas.Canvas,
						slides: List[Slide]):
		for slide in slides:
			self.__render_slide(slide)
			self.__pdf_finish_page(pdf)

	def __render_slide(self, slide: Slide):
		lay = Layout(slide, (self.size[0], self.size[1]))
		coords = lay.get_coords()
		for key, coord in coords.items():  # For each available items types
			drawer = self.drawers[key]  # Get the drawer
			for i, c in enumerate(coord):
				drawer(self.pdf, slide.items[key][i], c)


				# ? ALL THOSE 3 THINGS ARE HARD CODED FOR NOW	
				progress_thickness = self.slides.configs.settings["progress-thickness"]
				progress_pos_y = self.size[1] - (progress_thickness / 2)
				text_height = self.size[1] - progress_thickness - 10	

				# ! SLIDES NUMBER
				self.pdf.setFont(self.font_name, 30)
				self.pdf.drawString(self.size[0] - 100,
									text_height,
									f"{self.current_page} / {len(self.lst_slides)}")

				# ! AUTHOR
				self.pdf.drawString(30,
									text_height,
									f"{slide.configs.settings['author']}")
				
				# ! PROGRESS BAR
				part_done = self.current_page / len(self.lst_slides)
				self.pdf.setStrokeColorRGB(0.2, 0.2, 0.2)
				self.pdf.setLineWidth(progress_thickness)
				self.pdf.line(0, progress_pos_y, self.size[0] * part_done, progress_pos_y)
				self.pdf.setStrokeColorRGB(0.5, 0.5, 0.5)
				self.pdf.line(self.size[0] * part_done, progress_pos_y, self.size[0], progress_pos_y)

	def __draw_paragraph(self, 
						 pdf: canvas.Canvas, 
						 paragraph: str, 
						 coord: Tuple[int, int, int, int]):
		"""
		This draws a paragraph
		args:
			pdf (canvas.Canvas) : 
				pdf to add the paragraph to
			paragraph (str) : 
				paragraph to draw
			coord (Tuple[int, int, int, int]) : 
				(x, y, max_width, max_height)

		"""
		cx, cy, mw, mh = coord
		# ? This is the style of the paragraph
		styles = getSampleStyleSheet()
		styleN = styles["Normal"]
		styleN.fontName = self.font_name
		styleN.fontSize = self.default_fontsize
		styleN.leading = self.default_fontsize * 1.5
		styleN.alignment = 4  # HARD CODED JUSTIFIED BECAUSE ITS DA BEST

		p = Paragraph(paragraph, styleN)
		w, h = p.wrapOn(pdf, mw, mh)

		# Need some tricks to center because of their shitty bottomup system
		x = cx - w / 2
		y = cy - h + self.default_fontsize * 2 - h / 2
		p.drawOn(self.pdf, x, y)

	def __draw_title(self, 
					 pdf: canvas.Canvas, 
					 title: str,
					 coord: Tuple[int, int]):
		"""
		This sets the font size accroding to the depth of the title
		and draws the title and resets the font size
		args:
						pdf (canvas.Canvas) : 
							pdf to add the titles to
						title (str) : 
							title to draw
						coord (tuple) : 
							(x, y)
		"""
		title, title_size = self.configs.get_title_font_size(title)

		# ? This chooses the font size according to the depth of the title
		pdf.setFont(self.font_name, title_size)
		pdf.drawCentredString(coord[0], coord[1], title)
		pdf.setFont(self.font_name, self.default_fontsize)

	def __draw_image(self, 	
					 pdf: canvas.Canvas, 
					 image_obj: str, coord: 
					 Tuple[int, int, int, int]):
		"""
		This draws an image
		args:
						pdf (canvas.Canvas) : 
							pdf to add the image to
						image_obj (str) : 	
							Markdown image (![]())
						coord (Tuple[int, int, int, int]) : 
							(x, y, max_width, max_height)
		"""
		# TODO: Add caption under the image
		from PIL import Image

		cx, cy, mw, mh = coord

		# Extract the image from md line
		# ! Little hack for now, to be able to give a direct path to the image
		if image_obj.startswith("!"):
			img_path = image_obj.split("(")[1].split(")")[0]
		else:
			img_path = image_obj
		img = Image.open(img_path).transpose(Image.FLIP_TOP_BOTTOM)
		img = ImageReader(img)

		iw, ih = img.getSize()
		ar = float(iw) / float(ih)  # Aspect ratio

		if ar > float(mw) / float(mh):
			sf = float(mw) / float(iw)
		else:
			sf = float(mh) / float(ih)

		nw = int(iw * sf)
		nh = int(ih * sf)

		x = cx - nw / 2
		y = cy - nh / 2

		# Rotate the canvas when drawing the image because of their shitty bottomup system
		pdf.drawImage(img, x, y, width=nw, height=nh)

	# TODO : Maybe merge both type of lists because they feel pretty similar
	def __draw_olist(self, 
					 pdf: canvas.Canvas, 
					 olist: List[str], 
					 coord: Tuple[int, int, int, int]):
		"""
		This draws an ordered list
		args:
						pdf (canvas.Canvas) : 
							pdf to add the list to
						olist (list[str]) : 
							ordered list to draw
						coord (Tuple[int, int, int, int]) : 
							(x, y, max_width, max_height)
		"""
		cx, cy, mw, mh = coord

		styles = getSampleStyleSheet()
		styleN = styles["Normal"]
		styleN.fontName = self.font_name
		styleN.fontSize = self.default_fontsize
		styleN.leading = self.default_fontsize * 1.5
		styleN.alignment = 4  # Left aligned

		p = Paragraph("<br/>".join(olist), styleN)
		w, h = p.wrapOn(pdf, mw, mh)

		# Need some tricks to center because of their shitty bottomup system
		x = cx - w / 2
		y = cy - h + self.default_fontsize * 2 - h / 2
		p.drawOn(self.pdf, x, y)

	def __draw_ulist(self, 
					 pdf: canvas.Canvas, 
					 olist: List[str], 
					 coord: Tuple[int, int, int, int]):
		"""
		This draws an unordered list
		args:
						pdf (canvas.Canvas) : 
							pdf to add the list to
						olist (List[str]) : 
							unordered list to draw
						coord (Tuple[int, int, int, int]) : 
							(x, y, max_width, max_height)
		"""
		cx, cy, mw, mh = coord

		styles = getSampleStyleSheet()
		styleN = styles["Normal"]
		styleN.fontName = self.font_name
		styleN.fontSize = self.default_fontsize
		styleN.leading = self.default_fontsize * 1.5
		styleN.alignment = 4  # Left aligned

		p = Paragraph("<br/>".join(olist), styleN)
		w, h = p.wrapOn(pdf, mw, mh)

		# Need some tricks to center because of their shitty bottomup system
		x = cx - w / 2
		y = cy - h + self.default_fontsize * 2 - h / 2
		p.drawOn(self.pdf, x, y)

	def __draw_code(self, 
					pdf: canvas.Canvas, 
					code: str, 
					coord: Tuple[int, int, int, int]):
		"""
				This creates an image of the code with
				carbon.now.sh and and draws it on the pdf
				args:
								pdf (canvas.Canvas) : 
									pdf to add the code to
								code (str) : 
									code to draw
								coord (Tuple[int, int, int, int]) : 
									(x, y, max_width, max_height)
				returns:
								None
		"""
		from img_code import code2image

		# Temp, used to generate the image of the code
		code_path = code2image(code, "examples/assets/codes")

		self.__draw_image(self.pdf, code_path, coord)

	def __pdf_setup(self, 
					pdf: canvas.Canvas, 
					configs: Config):
		self.pdf.setAuthor(self.configs.settings["author"])
		self.pdf.setTitle(self.configs.settings["title"])
		self.pdf.setSubject(self.configs.settings["date"])

		self.font_name = self.configs.settings["font"].split(
			"/")[-1].split(".")[0]
		pdfmetrics.registerFont(
			TTFont(self.font_name, configs.settings["font"]))
		self.pdf.setFont(self.font_name, self.default_fontsize)

	def __pdf_finish_page(self, 
						  pdf: canvas.Canvas):
		self.pdf.showPage()
		self.current_page += 1

	def __pdf_save(self, 
				   pdf: canvas.Canvas):
		self.pdf.save()
