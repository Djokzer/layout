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


# TODOs
[ ] LAYOUT : Titled content (sub titles are for the main items)
[ ] LAYOUT : Double scalable, with markdown parameters
[ ] LAYOUT : Make a growable vertical and horizontal layout with n main items
[ ] Parse the content differently to pick a layout in markdown
[ ] Parse the paragraphs differently to pick an alignment
[ ] Abstract the titles for layouts with main(s)

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
- Only allow one title per item number



# Sources and Inspirations
Report lab docs : https://docs.reportlab.com/   
Carbon API : https://github.com/ShivangKakkar/Carbon   
Slide terminal : https://github.com/maaslalani/slides    
Suckless Sent : https://tools.suckless.org/sent/   
Best font : https://fonts.google.com/specimen/Economica   
