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

def get_third_filter_prompt(batch_text):
    return (
        f"You are filtering research papers. I will give you their concatenation of title + abstract + keywords.\n\n"
        f"Only return titles of the papers that match ALL of the following inclusion criteria:\n"
        f"- The primary target population must be higher education students and educators (NOT experts, librarians, administrative staff, or other stakeholders)\n"
        f"- The data must be directly collected from students and educators (NOT from documents, websites, databases, etc.)\n"
        f"- The topic must be directly related to the teaching and learning process\n"
        f"- The paper must focus specifically on challenges, risks, problems, or issues in integrating AI into teaching and learning\n\n"
        f"Exclude any paper that matches ANY of the following:\n"
        f"- Bibliometric analysis\n"
        f"- Systematic review\n"
        f"- Literature review\n"
        f"- Scoping review\n"
        f"- Critical review\n"
        f"- Editorials\n"
        f"- Interviews with a specific person\n\n"
        f"For the following papers:\n\n{batch_text}\n\n"
        f"Return only the exact titles (one per line) of the papers that meet ALL inclusion criteria and NONE of the exclusion criteria.\n")