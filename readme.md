# Layout
I want to build an easy tool to create beautiful presentation with simple markdown based syntax. A simple layout would be estimated from the slide content. 


## Unit tests
```bash
pytest test.py -v
```


## Sources
https://docs.reportlab.com/


## Random sample codes

```py
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# create a new PDF document with a custom background color
pdf = canvas.Canvas("example.pdf", pagesize=letter)
pdf.setFillColor(HexColor("#ffcc00"))
pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

# set the font color and type
pdf.setFont("Helvetica-Bold", 14)
pdf.setFillColor(HexColor("#333333"))

# add some text to the document
text = "Hello, world!"
pdf.drawCentredString(letter[0]/2, letter[1]/2, text)

# save the PDF document
pdf.save()
```


Custom shapes n all
```py
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame

# create a new PDF document with a custom background color
pdf = canvas.Canvas("example.pdf", pagesize=letter)
pdf.setFillColor(HexColor("#ffcc00"))
pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

# set up the layout
styles = getSampleStyleSheet()
style = styles["Normal"]
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras aliquet euismod ipsum, at tristique nibh hendrerit eu. Suspendisse interdum leo vel massa semper, et auctor libero semper."

frame = Frame(
    x1=1*inch,
    y1=1*inch,
    width=6*inch,
    height=8*inch,
    showBoundary=0
)

# add some text to the document
para = Paragraph(text, style)
frame.addFromList([para], pdf)

# save the PDF document
pdf.save()
```

CUSTOM FONT
```py
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# register the font
pdfmetrics.registerFont(TTFont("MyFont", "path/to/my/font.ttf"))

# set the font
pdf.setFont("MyFont", 14)
```


