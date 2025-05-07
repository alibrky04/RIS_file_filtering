def get_filter_prompt(batch_text):
	return (
		f"You are filtering research papers. Only return titles that match this criteria:\n\n"
		f"- Research papers about the ethics, risks, and challenges of AI use in higher education\n"
		f"- Exclude: literature reviews, theoretical frameworks, or conceptual analyses\n\n"
		f"For the following papers:\n\n{batch_text}\n\n"
		f"Return only the exact titles (one per line) of the papers that match."
	)