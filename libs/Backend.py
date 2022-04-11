def find_key(dictionary: dict, text: str):
	weighted_pass = {}

	def sub_string_search(text: str, name: str, password: str):

		def get_max_val(text: str, name: str, priority: float):
			"""
			Weights password based on length of searched text and no. of matching letters in the passwords.
			"""
			return max(len(text)/len(name), max_value) + priority

		name_wo_space = name.replace(" ", "")
		text_wo_space = text.replace(" ", "")
		case_insensitive_text, case_insensitive_name = text.lower(), name.lower()
		max_value = 0
		if text == name_wo_space:
			return True
		else:
			if case_insensitive_name.startswith(case_insensitive_text):
				max_value = get_max_val(case_insensitive_text, case_insensitive_name, 0.15)
			else:
				if text in name:  # Just checks if letteres searched are substring of the key in dictionary.
					max_value = get_max_val(text, name, priority=0)

				if case_insensitive_text in case_insensitive_name:  # Weights passwords without checking case.
					max_value = get_max_val(text = case_insensitive_text, name=case_insensitive_name, priority=0)

				if text in name_wo_space:  # Removes spaces from keys then checks whether text is found.
					max_value = get_max_val(text, name=name_wo_space, priority= -0.01)

				if text_wo_space in name_wo_space:  # Removes spaces both searched text and key and then weights password.
					max_value = get_max_val(text=text_wo_space, name=name_wo_space, priority= -0.02)
				
				if max_value>0.1: # If no letters match don't add.
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
		
		def get_max_ordered_value(search_text: str, name: str, priority: float):
			"""
			Checks for matching subsequences found in the searched text.
			Like "abcef" in "abcdef" and vice-versa.
			"""
			matching_letter = 0
			min_length = min(len(search_text), len(name))
			max_length = max(len(search_text), len(name))
			search_index = 0
			for index in range(min_length):
				if search_text[search_index] == name[index]:
					matching_letter += 1
					search_index += 1
				else:
					matching_letter -= 0.05

			max_matching = matching_letter 
			key_index = matching_letter = 0
			for index in range(min_length):
				if search_text[index] == name[key_index]:
					matching_letter += 1
					key_index += 1
				else:
					matching_letter -= 0.05
			
			max_matching= max(matching_letter, max_matching)
			return (max_matching / max_length) + priority

		
		max_val = max(
			get_max_val(text, name, -0.04), 
			get_max_ordered_value(text, name, -0.07)
			)

		lower_text = text.lower()
		lower_name = name.lower()
		max_val = max(
			get_max_val(lower_text, lower_name, -0.05), 
			get_max_ordered_value(lower_text, lower_name, -0.08), 
			max_val
			)

		nospace_text = text.replace(" ","")
		nospace_name = name.replace(" ","")
		max_val = max(
			get_max_val(nospace_text, nospace_name, -0.06), 
			get_max_ordered_value(nospace_text, nospace_name, -0.09), 
			max_val
			)
		if max_val> 0.1:
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

