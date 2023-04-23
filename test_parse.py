# UNIT TESTS
# Author : Jonas S.

from slides import Slides
from slide import Slide

import unittest

PATH_TESTS = "tests"

class Code(unittest.TestCase):
	
	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_code.md")
	
	# TEST CODES
	def test_single_code_block(self):
		self.assertEqual(self.s.slides[0].items["codes"][0], '```python\ndef foo():\n\tprint("Hello Graham!")\n```')

	def test_multiple_code_blocks(self):
		self.assertEqual(self.s.slides[1].items["codes"][0], '```c\nint main()\n{\n\tprintf("Hello Graham!\\n");\n}\n```')
		self.assertEqual(self.s.slides[1].items["codes"][1], '```rust\nfn main()\n{\n\tprintln!("Hello Graham!");\n}\n```')

	def test_multiple_code_blocks_with_mess(self):
		self.assertEqual(self.s.slides[2].items["codes"][0], '```c\nint main()\n{\n\tprintf("Hello Graham!\\n");\n}\n```')
		self.assertEqual(self.s.slides[2].items["codes"][1], '```rust\nfn main()\n{\n\tprintln!("Hello Graham!");\n}\n```')

class Olist(unittest.TestCase):
	
	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_olist.md")

	def test_single_olist(self):
		self.assertEqual(self.s.slides[0].items["olists"][0], ["1. Hello", "2. From", "3. Graham"])

	def test_multiple_olists(self):
		self.assertEqual(self.s.slides[1].items["olists"][0], ["1. Graham", "2. is", "3. God"])
		self.assertEqual(self.s.slides[1].items["olists"][1], ["1. Graham", "2. is", "3. Life"])

	def test_multiple_olists_with_mess(self):
		s = Slides(f"{PATH_TESTS}/test_olist.md")
		self.assertEqual(self.s.slides[2].items["olists"][0], ["1. Graham", "2. is", "3. God"])
		self.assertEqual(self.s.slides[2].items["olists"][1], ["1. Graham", "2. is", "3. Life"])

class Ulist(unittest.TestCase):
	
	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_ulist.md")

	def test_single_ulist(self):
		self.assertEqual(self.s.slides[0].items["ulists"][0], ["- Hello", "- From", "- Graham"])

	def test_multiple_ulists(self):
		self.assertEqual(self.s.slides[1].items["ulists"][0], ["- Graham", "- is", "- God"])
		self.assertEqual(self.s.slides[1].items["ulists"][1], ["- Graham", "- is", "- Life"])

	def test_multiple_ulists_with_mess(self):
		s = Slides(f"{PATH_TESTS}/test_ulist.md")
		self.assertEqual(self.s.slides[2].items["ulists"][0], ["- Graham", "- is", "- God"])
		self.assertEqual(self.s.slides[2].items["ulists"][1], ["- Graham", "- is", "- Life"])

class Title(unittest.TestCase):

	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_title.md")

	def test_single_title(self):
		self.assertEqual(self.s.slides[0].items["titles"], ["# Title", "## Subtitle", "### Subsubtitle", "#### Subsubsubtitle"])
	
	def test_multiple_titles_with_mess(self):
		self.assertEqual(self.s.slides[1].items["titles"], ["# Title", "## Subtitle", "### Subsubtitle", "#### Subsubsubtitle",
					     						   "# Second Title", "## Second Subtitle", "### Second Subsubtitle", "#### Second Subsubsubtitle"])
		

class Image(unittest.TestCase):

	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_image.md")

	def test_single_image(self):
		self.assertEqual(self.s.slides[0].items["images"], ["![Test image](https://picsum.photos/200/300)"])
	
	def test_multiple_images_with_mess(self):
		self.assertEqual(self.s.slides[1].items["images"], ["![Test image 1](https://picsum.photos/200/300)", "![Test image 2](https://picsum.photos/300/200)"])

class Paragraphs(unittest.TestCase):

	def setUp(self):
		self.s = Slides(f"{PATH_TESTS}/test_paragraph.md")

	def test_single_paragraph(self):
		self.assertEqual(self.s.slides[0].items["paragraphs"], ["MEET GRAHAM THE ONLY PERSON DESIGNED TO SURVIVE ON OUR ROADS As much as we like to think we're invincible, we're not. But what if we were to change? What if our bodies were built to survive a low impact crash? What might we look like? The result of these questions is Graham, a reminder of just how vulnerable our bodies really are."])
	
	def test_multiple_paragraphs_with_mess(self):
		self.assertEqual(self.s.slides[1].items["paragraphs"], ["This is the first simple paragraph", "on multiple lines, but these are in multiple list items", "This is the second simple paragraph", "on multiple lines again, but these are in multiple list items"])