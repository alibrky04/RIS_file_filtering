import os
import glob
import json
from openai import OpenAI
import dataManager
import prompts

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

model = "gpt-4.1-mini-2025-04-14"
temperature = 0.2
max_tokens = 10000
topic = "paper_filtering"
input_file = "input/pdfs"
output_file = "output/results.json"
filtered_metadata_file = ""

def call_api(prompt):
	response = client.chat.completions.create(
		model=model,
		messages=[{"role": "user", "content": prompt}],
		temperature=temperature,
		max_tokens=max_tokens
	)
	return response.choices[0].message.content.strip()

def save_results(titles):
	with open(output_file, 'a', encoding='utf-8') as f:
		f.write(titles + '\n')

def ris_filter():
	papers = dataManager.parse_ris(input_file)
	batches = dataManager.batch_papers(papers)

	for i, batch in enumerate(batches):
		print(f"Processing batch {i+1}/{len(batches)}...")
		batch_text = dataManager.format_batch_for_prompt(batch)
		prompt = prompts.get_third_filter_prompt(batch_text)
		try:
			result = call_api(prompt)
			save_results(result)
		except Exception as e:
			print(f"Error on batch {i+1}: {e}")

def analyze_pdf(pages, doc_id):
	prompt = prompts.build_analysis_prompt(pages)
	result = call_api(prompt)
	data = json.loads(result)
	data["ID"] = doc_id
	return data

def process_all_pdfs(pdf_dir, output_path="output/results.json"):
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
	all_data = []

	for pdf_path in pdf_files:
		doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
		print(f"📘 Processing: {doc_id}")
		pages = dataManager.extract_pdf_pages(pdf_path)
		try:
			data = analyze_pdf(pages, doc_id)
			all_data.append(data)
		except Exception as e:
			print(f"❌ Error processing {doc_id}: {e}")

	with open(output_path, 'w', encoding='utf-8') as f:
		json.dump(all_data, f, indent=2, ensure_ascii=False)
	print(f"✅ All data saved to {output_path}")

if __name__ == "__main__":
	# ris_filter()
	process_all_pdfs(input_file, output_file)
	dataManager.json_to_excel(output_file, "output/results.xlsx")
	# dataManager.extract_filtered_metadata(input_file, output_file, filtered_metadata_file)
	# dataManager.find_missing_titles(filtered_metadata_file, output_file)
	# dataManager.compare_ris_files(filtered_metadata_file, "Second_Data/final_result.ris", "output")
