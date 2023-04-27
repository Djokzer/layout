from slides import Slides
from config import Config
from renderer import Renderer
from typing import List, Tuple, Dict

def main():
	s = Slides("simple.md")
	configs, ps = s.get()
	print(f"PARAGRAPHS :  {ps[1].paragraphs}")
	print(f"TITLES  : {ps[1].titles}")
	print(f"CODE    : {ps[1].code}")
	print(configs)

def report():
	from reportlab.lib.pagesizes import letter, landscape
	from reportlab.lib.colors import HexColor
	from reportlab.pdfgen import canvas
	from reportlab.lib.styles import getSampleStyleSheet
	from reportlab.lib.units import inch
	from reportlab.platypus import Paragraph, Frame

	# create a new PDF document with a custom background color
	pdf = canvas.Canvas("example.pdf", pagesize=landscape(letter))
	pdf.setFillColor(HexColor("#282C34"))
	pdf.rect(10, 10, letter[0], letter[1], fill=True, stroke=True)

	# set up the layout
	styles = getSampleStyleSheet()
	style = styles["Normal"]
	style.textColor = HexColor("#ABB2BF")
	style.fontSize = 30
	text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras aliquet euismod ipsum, at tristique nibh hendrerit eu. Suspendisse interdum leo vel massa semper, et auctor libero semper."

	# Add an image
	#pdf.drawImage("image.png", 0, 0, width = 2 * inch, height = 4 * inch)

	frame = Frame(
		x1 = 1 * inch,
		y1 = 1 * inch,
		width = 6 * inch,
		height =8 * inch,
		showBoundary = 0
	)

	# add some text to the document
	para = Paragraph(text, style)
	frame.addFromList([para], pdf)

	# save the PDF document
	pdf.save()


def test1():
	
	s = Slides("single_slide.md")
	r = Renderer("nomain.pdf", s, (1920, 1080))




if __name__ == "__main__":
	test1()