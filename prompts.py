def get_first_filter_prompt(batch_text):
	return (
		f"You are filtering research papers. I will give you their concecation of title+abstract+keywords.\n\n"
		f"Only return titles of the papers that match this criteria:\n\n"
		f"- Research papers about the ethics, risks, and challenges of AI use in higher education\n"
		f"- Exclude: literature reviews, theoretical frameworks, or conceptual analyses\n\n"
		f"For the following papers:\n\n{batch_text}\n\n"
		f"Return only the exact titles (one per line) of the papers that match."
	)

def get_second_filter_prompt(batch_text):
	return (
		f"You are filtering research papers. I will give you their concecation of title+abstract+keywords.\n\n" 
		f"Only return titles of the papers that match this criteria:\n\n"
		f"- Research papers that gives detailed analysis of the ethics, risks, and challenges of" 
		f"AI use in higher education in their abstract\n"
		f"- Exclude: literature reviews, theoretical frameworks, or conceptual analyses\n\n"
		f"For the following papers:\n\n{batch_text}\n\n"
		f"Return only the exact titles (one per line) of the papers that match.\n\n"
	)