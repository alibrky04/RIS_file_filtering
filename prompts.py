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

def build_analysis_prompt(pages):
	context = "\n\n".join(f"[Page {p['page']}]\n{p['text']}" for p in pages)

	return f"""
  You are an academic assistant. You will be given a research paper split into pages. Your task is to extract specific information using **only the original text from the paper**—do not rephrase or summarize.

  For each field in the JSON below, follow these detailed instructions:

  1. **Title**: Extract the paper's title verbatim.

  2. **Purpose**: Find the section(s) that describe the objective, aim, or purpose of the paper. Use the original paragraph(s). Provide each with its page number.

  3. **Results**: This field should ONLY contain text that directly discusses the *challenges*, *risks*, or *ethical implications* of using artificial intelligence in higher education. Extract relevant statements or paragraphs and indicate their page numbers.

  4. **Target Population**: Identify the target audience or population studied (e.g., students, faculty, specific universities). If explicitly mentioned, quote it; if not, infer carefully from context and specify the original wording.

  5. **Methodology**: If a methodology is explicitly described, extract the original paragraph(s) where it is explained, and include the page number(s). If not, carefully infer the likely methodology and describe it in 1–2 lines.

  6. **Field of Study**: Identify the academic or application domain where AI is applied in this paper (e.g., medical education, computer science education). Use wording from the paper if possible.

  Use this exact JSON format and populate it fully (quotes where applicable, page numbers for Purpose, Results, and Methodology):

  {{
    "ID": "<document id>",
    "Title": "...",
    "Purpose": [{{"page": X, "text": "..."}}],
    "Results": [{{"page": X, "text": "..."}}],
    "Target Population": "...",
    "Methodology": [{{"page": X, "text": "..."}}] or "Likely methodology: ...",
    "Field of Study": "..."
  }}

  Here is the content of the paper:

  {context}
  """

def pdf_filter_prompt(pages):
	context = "\n\n".join(f"[Page {p['page']}]\n{p['text']}" for p in pages)

	return (
		"You are a research paper filter. I will give you the full text of a paper, extracted from a PDF and organized by page.\n\n"
		"Return **'YES'** only if the paper satisfies **ALL** of the following inclusion criteria:\n"
		"- The **primary target population** is higher education students and educators (NOT experts, librarians, admin staff, or other stakeholders)\n"
		"- The **data is collected directly** from students and educators (NOT from documents, websites, or secondary sources)\n"
		"- The **topic** is directly related to **teaching and learning** in higher education\n"
		"- The paper discusses **challenges, risks, or issues** of integrating AI into the teaching and learning process\n\n"
		"Exclude the paper if it matches **ANY** of the following:\n"
		"- Bibliometric analysis\n"
		"- Systematic review, literature review, or scoping review\n"
		"- Critical review\n"
		"- Editorials\n"
		"- Interviews with a specific individual (e.g., one professor)\n\n"
		"Here is the paper:\n\n"
		f"{context}\n\n"
		"First, respond with **'YES'** or **'NO'** to indicate whether the paper meets the criteria.\n"
		"Then, in **2 to 3 sentences**, briefly explain the reasoning behind your decision, based on the content of the paper.\n"
	)

def pdf_country_prompt(pages):
    context = "\n\n".join(f"[Page {p['page']}]\n{p['text']}" for p in pages)

    return (
        "You are a research paper filter. I will give you the full text of a paper, extracted from a PDF and organized by page.\n\n"
        "Return the **country** where the research was conducted, based on the content of the paper, in the following JSON format:\n\n"
        "{\n"
        "  \"Country\": [\"Country1\", \"Country2\"]\n"
        "}\n\n"
        "Here is the paper:\n\n"
        f"{context}\n\n"
        "If the country is not explicitly mentioned, infer it from the context. If you cannot determine the country, respond with **'Unknown'**. "
        "If multiple countries are mentioned, list them all in the 'Country' array."
    )

def json_summarize_prompt(json_data):
	return (
		f"""You will receive a JSON object representing a research paper.

Your task is to:
1. Summarize the **Purpose** field into **1 to 3 concise sentences**.
2. Summarize the **Results** field into **2 to 3 informative paragraphs**.
3. Summarize the **Methodology** field into **1 to 2 concise paragraphs**.
4. Leave all other fields unchanged.
5. Return the result as a valid JSON object in the same structure, but remove any page information.

Here is the input JSON object:
{json_data}

Only return the transformed JSON object, and nothing else."""
	)