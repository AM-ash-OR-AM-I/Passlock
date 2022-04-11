def find_key(dictionary: dict, text: str):
	weighted_pass = {}

	def sub_string_search(text: str, name: str, password: str):
		
		def is_initial_substring(text: str, name: str):
			"""
			Checks if the searched text is in the beginning of the password name.
			"""
			for ind in range(len(text)):
				if text[ind] != name[ind]:
					return False
			return True

		def get_max_val(text: str, name: str, priority: float):
			"""
			Weights password based on length of searched text and no. of matching letters in the passwords.
			"""
			return max(len(text)/len(name), max_value) + priority

		name_wo_space = name.replace(" ", "")
		text_wo_space = text.replace(" ", "")
		case_insensitive_text, case_insensitive_name = text.lower(), name.lower()
		max_value = 0
		if text == name or text == name_wo_space:
			return True
		else:
			if is_initial_substring(case_insensitive_text, case_insensitive_name):
				# Higher priority is given if searched text is at the beginning.
				max_value = get_max_val(case_insensitive_text, case_insensitive_name, 0.1)
			else:
				if text in name:  # Just checks if letteres searched are substring of the key in dictionary.
					max_value = get_max_val(text, name, priority=0)

				if case_insensitive_text in case_insensitive_name:  # Weights passwords without checking case.
					max_value = get_max_val(text = case_insensitive_text, name=case_insensitive_name, priority=0)

				if text in name_wo_space:  # Removes spaces from keys then checks whether text is found.
					max_value = get_max_val(text, name=name_wo_space, priority= -0.01)

				if text_wo_space in name_wo_space:  # Removes spaces both searched text and key and then weights password.
					max_value = get_max_val(text=text_wo_space, name=name_wo_space, priority= -0.02)
				
				if max_value>0: # If no letters match don't add.
					weighted_pass[(name, password)] = max_value

			return False
	
	def fuzzy_search(text: str, name: str, password: str):
		def get_max_val(search_text: str, name: str, priority: float):
			matching_letter = 0
			min_length = min(len(search_text), len(name))
			max_length = max(len(search_text), len(name))
			for index in range(min_length):
				if search_text[index] == name[index]:
					matching_letter += 1
			return (matching_letter / max_length) + priority
		
		max_val = get_max_val(text, name, -0.04)
		max_val = max(get_max_val(text.lower(), name.lower(), -0.05), max_val)
		max_val = max(get_max_val(text.replace(" ",""), name.replace(" ",""), -0.06), max_val)
		if max_val> 0:
			weighted_pass[(name, password)] = max_val
		
	
	def sort_keys(key_dict: dict):
		key_arr = list(key_dict.items())
		key_arr.sort(key=lambda x: x[1], reverse=True)  # Sorts the list based on the weighted values.
		return key_arr

	
	if text in dictionary or text.lower() in dictionary or text.upper() in dictionary:
		return [(text, dictionary[text])]
	else:
		for name, password in dictionary.items():
			# If text equals password without space then it returns that, else checks all passwords.
			
			if sub_string_search(text, name, password):
				return [(name, password)]
		
		if not weighted_pass:
			for name, password in dictionary.items():
				# Uses approximate search to find the password.
				
				fuzzy_search(text, name, password)

	
	return sort_keys(weighted_pass)

