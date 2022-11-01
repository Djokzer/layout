---
configs
---

## Titles and subs
```md
# Title
## Subtitle
```

## Separators
```m
||| <- Vertical separator
--- <- Horizontal separator
```

## Layouts
### Layout 1 (Simple Text)
```md
[1]
# BIG TITLE
Just a simple paragaph taking as much space as it wants.
```

```md
[1] 
# BIG TITLE
- Simple
	- subList included
	- subList included
- List 
	- subList included
	- subList included
- Of 
- Words
```

```md
[1] <- Layout 1
## SMALLER TITLE CAUSE I CAN
1. Simple
	1. subList included
	2. subList included
	3. subList included
2. List 
	1. subList included
	2. test
	3. subList included
3. Of 
4. Words 
```

### Layout 2 (Double content)
```md
[2] <- Layout 2
# This is an images by the side of text or list
![img/image.png](img/image.png)
1. Simple
2. List
3. Of
4. Words
```

```md
[2] <- Layout 2
# This is 2 images side by side
![img/image.png](img/image.png)
![img/image2.png](img/image2.png)
```

### Layout 3 (Code) 

```md
[3] <- Layout 3
# This is some c code
c[3-5]
int main(int argc, char** argv)
{
	printf("Graham\n");
}
```

## Fragments
You fragment what you want with `[frag]`

### Example of fragments

```md
# BIG TITLE
[frag]
- Simple
[frag]
- List 
[frag]
- Of 
[frag]
- Words
```

These elements of the list will come one by one



