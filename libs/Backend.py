class Backend:
	def find_password(self, dictionary, text):
		if text in dictionary or text.lower() in dictionary or text.uppper() in dictionary:
			return [(text, dictionary[text])]
		else:
			for text, password in dictionary.items():
				text = text.replace(" ", "")
