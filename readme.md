# Layout

I want to build an easy tool to create beautiful presentation with simple markdown based syntax. The tool would use the [https://revealjs.com/](https://revealjs.com/) Framework.



## Parsing
### Slides
1. There is a First split that returns a list of chunk of slides, these are `columns`. Each columns can contain multiples vertical slides.

2. We then split each of these columns into individual slides.

We can now split these slides into lines and parse them.

### 2 items centered 
```html
<section>
	<div style="text-align: center; float: left; width: 40%;">
	<ul>
			<li>Item 1</li>
			<li>Item 2</li>
			<li>Item 3</li>
	</ul>
	</div>

	<div style="text-align: center; float: right; width: 40%;">
		<ol>
			<li> Item 1</li>
			<li> Item 2</li>
			<li> Item 3</li>
		</ol>
	</div>
</section>
````

