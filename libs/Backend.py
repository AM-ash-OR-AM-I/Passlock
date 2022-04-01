def find_key(dictionary: dict, text: str):
	weighted_pass = {}

	def weight_passwords_1(text: str, name: str, password: str):
		def get_max_val(text: str, name: str, priority: float):
			"""
			Weights password based on length of searched text and actual no. of letters in the passwords.
			"""
			return max(len(text)/len(name), max_value) + priority

		name_wo_space = name.replace(" ", "")
		text_wo_space = text.replace(" ", "")
		case_insensitive_text, case_insensitive_name = text.lower(), name.lower()
		max_value = 0
		if text == name_wo_space:
			return True
		else:
			if text in name:  # Just checks if letteres searched are substring of the key in dictionary.
				max_value = get_max_val(text, name, priority=0)

			if case_insensitive_text in case_insensitive_name:  # Weights passwords without checking case.
				max_value = get_max_val(text = case_insensitive_text, name=case_insensitive_name, priority=0)

			if text in name_wo_space:  # Removes spaces from keys then checks whether text is found.
				max_value = get_max_val(text, name=name_wo_space, priority= -0.01)

			if text_wo_space in name_wo_space:  # Removes spaces both searched text and key and then weights password.
				max_value = get_max_val(text=text_wo_space, name=name_wo_space, priority= -0.02)
			
			
			if max_value>0:
				weighted_pass[(name, password)] = max_value
			return False
	
	def weight_passwords_2(text, name, password):
		pass

	
	def sort_keys(key_dict: dict):
		key_arr = list(key_dict.items())
		key_arr.sort(key=lambda x: x[1])  # Sorts the list based on the weighted values.
		# weighted_pass = key_arr


	
	if text in dictionary or text.lower() in dictionary or text.upper() in dictionary:
		return [(text, dictionary[text])]
	else:
		for name, password in dictionary.items():
			"""
			If text equals password without space then it returns that, else checks all passwords.
			"""
			if weight_passwords_1(text, name, password):
				return [(name, password)]
		
		if not weighted_pass:
			weight_passwords_2(text, name, )
	# sort_keys(weighted_pass)
	return weighted_pass

