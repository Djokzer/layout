class Config:
    def __init__(self, configs):
        
        # These are the default settings
        self.settings = {
            "author": "author",
            "title": "Title",
            "date": "01/01/2020",
            "theme": "",
            "font": "Arial",
            "font-size-text": 50,  		
            "font-size-title": 120,  	
            "progress-thickness": 15,
        }
        self.intable_settings = ["font-size-title", 
                                 "font-size-text", 
                                 "progress-thickness"]
        self.__parse(configs)

    def __parse(self, configs):
        """
        This parses the configs and fills the dictionary
        Args:
                configs (list[str]): list of configs
        Returns:
                None
        """
        for config in configs:
            config = config.replace(": ", ":")  # remove spaces
            key, value = config.split(":")
            # Int the settings that are supposed to be int
            if key in self.settings:
                if key in self.intable_settings:
                    value = int(value)
                self.settings[key] = value

    def get_title_font_size(self, title: str) -> tuple:
        """
                This takes a title and returns the font size
                and the title wihout the hashes,
                it selects a font size according to the number of hashes
                and the configured font-size-title
        Args:
                title (str) : title of the slide
        Returns:
                (str, int) : title without the '#'s, font size
        """
        parts = title.split(" ", 1)
        hashes = parts[0]
        title = parts[1]

        # ? This chooses the font size according to the depth of the title
        font_size = self.settings["font-size-title"] - (len(hashes) * 20)
        return title, font_size
