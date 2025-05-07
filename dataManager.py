import re

def parse_ris(filepath):
	with open(filepath, 'r', encoding='utf-8') as file:
		content = file.read()

	entries = content.strip().split('\nER  -')
	papers = []
	for entry in entries:
		title = extract_field(entry, 'TI')
		abstract = extract_field(entry, 'AB')
		keywords = extract_field(entry, 'KW', multi=True)
		if title:
			papers.append({
				'title': title,
				'abstract': abstract,
				'keywords': keywords
			})
	return papers

def extract_field(entry, tag, multi=False):
	pattern = rf'^{tag}  - (.+)$'
	matches = re.findall(pattern, entry, re.MULTILINE)
	if multi:
		return '; '.join(matches)
	return matches[0] if matches else ''

def batch_papers(papers, max_token_estimate=6000):
	batches = []
	batch = []
	token_count = 0

	for paper in papers:
		concat = f"{paper['title']}\n{paper['abstract']}\n{paper['keywords']}".strip()
		est_tokens = len(concat.split()) * 1.3
		if token_count + est_tokens > max_token_estimate and batch:
			batches.append(batch)
			batch = []
			token_count = 0
		batch.append(paper)
		token_count += est_tokens

	if batch:
		batches.append(batch)

	return batches

def format_batch_for_prompt(batch):
	formatted = []
	for paper in batch:
		text = f"Title: {paper['title']}\nAbstract: {paper['abstract']}\nKeywords: {paper['keywords']}".strip()
		formatted.append(text)
	return '\n\n'.join(formatted)

def extract_filtered_metadata(ris_path, filtered_titles_path, output_path):
	with open(filtered_titles_path, 'r', encoding='utf-8') as f:
		filtered_titles = {line.strip().lower() for line in f if line.strip()}

	with open(ris_path, 'r', encoding='utf-8') as file:
		content = file.read()

	entries = content.strip().split('\nER  -')
	matched_entries = []

	for entry in entries:
		entry += '\nER  -'
		title = extract_field(entry, 'TI')
		if title and title.strip().lower() in filtered_titles:
			matched_entries.append(entry.strip())

	with open(output_path, 'w', encoding='utf-8') as f:
		f.write('\n\n'.join(matched_entries))

	print(f"{len(matched_entries)} entries matched and written to {output_path}")

def find_missing_titles(ris_path, filtered_titles_path):
	with open(filtered_titles_path, 'r', encoding='utf-8') as f:
		filtered_titles = {line.strip().lower() for line in f if line.strip()}

	with open(ris_path, 'r', encoding='utf-8') as file:
		content = file.read()

	entries = content.strip().split('\nER  -')
	matched_titles = set()

	for entry in entries:
		title = extract_field(entry, 'TI')
		if title and title.strip().lower() in filtered_titles:
			matched_titles.add(title.strip().lower())

	missing_titles = filtered_titles - matched_titles

	print(f"Missing titles ({len(missing_titles)}):")
	for title in missing_titles:
		print(f"- {title}")