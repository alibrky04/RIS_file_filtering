import re
import fitz
import pandas as pd
import json

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

def extract_titles(ris_path):
	with open(ris_path, 'r', encoding='utf-8') as f:
		content = f.read()

	entries = content.strip().split('\nER  -')
	titles = set()

	for entry in entries:
		match = re.search(r'^TI  - (.+)$', entry, re.MULTILINE)
		if match:
			titles.add(match.group(1).strip().lower())
	return titles

def compare_ris_files(ris_a_path, ris_b_path, output_dir='output'):
	titles_a = extract_titles(ris_a_path)
	titles_b = extract_titles(ris_b_path)

	matched = sorted(titles_a & titles_b)
	unmatched = sorted(titles_a - titles_b)

	with open(f"{output_dir}/matched_titles.txt", 'w', encoding='utf-8') as f:
		f.write('\n'.join(matched))

	with open(f"{output_dir}/unmatched_titles.txt", 'w', encoding='utf-8') as f:
		f.write('\n'.join(unmatched))

	print(f"✅ Comparison Complete:")
	print(f"  Total in File A: {len(titles_a)}")
	print(f"  Matches in File B: {len(matched)}")
	print(f"  Not found in File B: {len(unmatched)}")

def extract_pdf_pages(pdf_path):
	doc = fitz.open(pdf_path)
	pages = []
	for i, page in enumerate(doc, start=1):
		text = page.get_text()
		if text.strip():
			pages.append({'page': i, 'text': text})
	return pages

def json_to_excel(json_path, excel_path):
	with open(json_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	records = []
	for item in data:
		base = {
			"ID": item.get("ID", ""),
			"Title": item.get("Title", ""),
			"Target Population": item.get("Target Population", ""),
			"Field of Study": item.get("Field of Study", "")
		}

		for key in ["Purpose", "Results", "Methodology"]:
			paragraphs = item.get(key, [])
			if isinstance(paragraphs, list):
				base[key] = "\n\n".join([f"[p.{p['page']}] {p['text']}" for p in paragraphs])
			else:
				base[key] = paragraphs or ""

		records.append(base)

	df = pd.DataFrame(records)
	df.to_excel(excel_path, index=False)
	print(f"✅ Excel saved to: {excel_path}")