class Config:

	def __init__(self, configs):
		self.settings = {
			"author": "",
			"title": "",
			"date": "",
			"theme": "",
			"font" : "",
		}
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
			config = config.replace(" ", "") # remove spaces
			key, value = config.split(":")
			if key in self.settings:
				self.settings[key] = value