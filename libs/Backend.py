from typing import Dict


def find_key(dictionary: Dict, text: str):
	weighted_pass = {}

	def weight_passwords(text, name, password):
		name_wo_space = name.replace(" ", "")
		lower_text, lower_name = text.lower(), name.lower()
		max_value = 0
		priority = 0
		if text == name_wo_space:
			return True
		else:
			if text in name or lower_text in lower_name:
				priority = 0
				max_value = max(len(text) / len(name), len(lower_text) / len(lower_name), max_value) + priority
			if text in name_wo_space:
				priority = -0.01
				max_value = max(len(text) / len(name), max_value) + priority

			if max_value>0:
				weighted_pass[(name, password)] = max_value
			return False

	def sort_keys(key_dict):
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
			if weight_passwords(text, name, password):
				return [(name, password)]

	# sort_keys(weighted_pass)
	return weighted_pass

