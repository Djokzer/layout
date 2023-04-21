# UNIT TESTS
# Author : Jonas S.

from slides import Slides
from slide import Slide

import unittest

PATH_TESTS = "tests"

class Code(unittest.TestCase):
	
	# TEST CODES
	def test_single_code_block(self):
		s = Slides(f"{PATH_TESTS}/test_code.md")
		self.assertEqual(s.slides[0].codes[0], '```python\ndef foo():\n\tprint("Hello Graham!")\n```')

	def test_multiple_code_blocks(self):
		s = Slides(f"{PATH_TESTS}/test_code.md")
		self.assertEqual(s.slides[1].codes[0], '```c\nint main()\n{\n\tprintf("Hello Graham!\\n");\n}\n```')
		self.assertEqual(s.slides[1].codes[1], '```rust\nfn main()\n{\n\tprintln!("Hello Graham!");\n}\n```')

	def test_multiple_code_blocks_with_mess(self):
		s = Slides(f"{PATH_TESTS}/test_code.md")
		self.assertEqual(s.slides[2].codes[0], '```c\nint main()\n{\n\tprintf("Hello Graham!\\n");\n}\n```')
		self.assertEqual(s.slides[2].codes[1], '```rust\nfn main()\n{\n\tprintln!("Hello Graham!");\n}\n```')

class Olist(unittest.TestCase):

	def test_single_olist(self):
		s = Slides(f"{PATH_TESTS}/test_olist.md")
		self.assertEqual(s.slides[0].olists[0], ["1. Hello", "2. From", "3. Graham"])

	def test_multiple_olists(self):
		s = Slides(f"{PATH_TESTS}/test_olist.md")
		self.assertEqual(s.slides[1].olists[0], ["1. Graham", "2. is", "3. God"])
		self.assertEqual(s.slides[1].olists[1], ["1. Graham", "2. is", "3. Life"])

	def test_multiple_olists_with_mess(self):
		s = Slides(f"{PATH_TESTS}/test_olist.md")
		self.assertEqual(s.slides[2].olists[0], ["1. Graham", "2. is", "3. God"])
		self.assertEqual(s.slides[2].olists[1], ["1. Graham", "2. is", "3. Life"])