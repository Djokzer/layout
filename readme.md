# Layout
Simple markdown to pdf presentation tool based on custom layouts

## Tests
```bash
pytest test.py -v
```

## Generate examples
Generate examples in examples folder:
```bash
python examples.py
```

## Pipeline

1. Parsing
2. Layout creation (gives pos of every items)
3. Rendering of items on pdf


### Files description
```
src
├── config.py
├── examples.py
├── img_code.py
├── layout.py
├── main.py
├── renderer.py
├── slide.py
├── slides.py
└── test_parse.py
```

#### Config 
- Config parsing
- Config defaults
- Where you add a new config

#### examples
- Create the example pdfs

#### img_code
- Create images from code
- Change code theme 

#### layout
- Where the layout is chosen
- Where the layout is parsed and outputs pos and size of main items
- Where the layouts are defined
- Where you add the layout(s)

#### main
- Not really used for now, use the examples

#### renderer
- Where the pdf is actually created
- Where each item is actually drawned with passed pos
- Where the page number, progress bar, and author are added

#### slide
- Where a single slide is parsed into items

#### slide
- Where the markdown is read
- Where the config is read
- Where each slides are separated and parsed


# TODOs
- [ ] Parse the content differently to pick a layout in markdown with parameters
- [ ] Abstract the titles for layouts with main(s)
- [ ] LAYOUT : Titled content (sub titles are for the main items)
- [ ] LAYOUT : Double scalable, with markdown parameters
- [ ] LAYOUT : Make a growable vertical and horizontal layout with n main items

## Possible Implementations

### Pick Custom layout 
Parse the markdown differently to allow custom layouts to be chosen, we can also pass parameters to the layout. There can be multiple parameters.


**syntax : [LAYOUT]{PARAMETERS}**


Example
```markdown
---
title: Simple
author: Handsome Graham
---

---[DOUBLE_SCALABLE]{70, 30}
# This is a custom layout slide

![This is graham, it should take 70% of the main content as mentionned in the layout parameter](graham_image.png)

This is a paragraph, its considered the second main content and thus will only be allowed to take 30% of the main content

---[TITLED_CONTENT]{true, true}
# This is a second slide with a titled content Layout
## This will be the title of the first main content
This paragraph is titled content, it will be the first and should take 50 % of the main content. We can notice parameters are passed to the layout to tell us if the title is showed or not.

## This will be the title of the second main content
- This is
- the second 
- main main content
- and it is also titled
```


### Layout : Titled content
<!--```markdown-->


### Layout : Double scalable
This might change due to the addition of growable vertical and horizontal layouts. There could be more parameters then


**syntax : [SCALABLE]{width1, width2, widthn}**

```markdown
---
title: Simple scalable layouts
---
random slide content


---[SCALABLE]{70, 30} 
# Random slide content with 2 main items
Random main content 1

![Random content 2](graham_image.png)

---[SCALABLE]{70, 30, 50} 
Random slide content with 3 main items

```

That would create a layout with 2 items, 
the first one taking 70% of the page and the second 30%

### Titled content

**syntax : [TITLED]{title1, title2}**

```markdown
---
title: Simple
author: Handsome Graham
---

---[TITLED]{"This is a title", "This is a second title"}
This is the first main titled content

This is a second main titled content

---

  
```


# Sources and Inspirations
Report lab docs : https://docs.reportlab.com/   
Carbon API : https://github.com/ShivangKakkar/Carbon   
Slide terminal : https://github.com/maaslalani/slides    
Suckless Sent : https://tools.suckless.org/sent/   
Best font : https://fonts.google.com/specimen/Economica   
