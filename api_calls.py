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

def call_api(prompt):
	response = client.chat.completions.create(
		model=model,
		messages=[{"role": "user", "content": prompt}],
		temperature=temperature,
		max_tokens=max_tokens
	)
	return response.choices[0].message.content.strip()

def save_results(titles, output_file):
	with open(output_file, 'a', encoding='utf-8') as f:
		f.write(titles + '\n')

def ris_filter(input_file):
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

def analyze_pdf(pages, doc_id, prompt_function):
    prompt = prompt_function(pages)
    result = call_api(prompt)
    result = result.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(result)
    data["ID"] = doc_id
    return data

def process_all_pdfs(pdf_dir, prompt_function, output_path="output/results.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    all_data = []

    for pdf_path in pdf_files:
        doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"📘 Processing: {doc_id}")
        pages = dataManager.extract_pdf_pages(pdf_path)
        try:
            data = analyze_pdf(pages, doc_id, prompt_function)
            all_data.append(data)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved for {doc_id}")

        except Exception as e:
            print(f"❌ Error processing {doc_id}: {e}")

    print(f"✅ All data saved to {output_path}")

def filter_pdfs_with_criteria(pdf_dir, output_path="output/pdf_filter_results.txt"):
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

	with open(output_path, 'a', encoding='utf-8') as f:
		for pdf_path in pdf_files:
			doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
			print(f"🧪 Filtering: {doc_id}")
			pages = dataManager.extract_pdf_pages(pdf_path)

			try:
				prompt = prompts.pdf_filter_prompt(pages)
				result = call_api(prompt)
				lines = result.strip().splitlines()
				decision = lines[0].strip().upper() if lines else "UNKNOWN"
				explanation = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

				if decision not in ("YES", "NO"):
					print(f"⚠️ Unexpected response from API for {doc_id}: {result}")
					decision = "UNKNOWN"
			except Exception as e:
				print(f"❌ Error filtering {doc_id}: {e}")
				decision = "ERROR"
				explanation = str(e)

			f.write(f"{doc_id}: {decision}\n{explanation}\n\n")
			f.flush()

	print(f"✅ Filter results saved incrementally to {output_path}")

def flatten_fields(obj, keys_to_flatten=["Purpose", "Results", "Methodology"]):
    for key in keys_to_flatten:
        if isinstance(obj.get(key), list):
            texts = [entry["text"] for entry in obj[key] if isinstance(entry, dict) and "text" in entry]
            obj[key] = "\n\n".join(texts)
    return obj

def summarize_json_results(input_path="output/results.json", output_path="output/summarized_results.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    summarized_data = []

    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            try:
                summarized_data = json.load(f)
            except:
                pass

    start_index = len(summarized_data)

    for i, paper in enumerate(data[start_index:], start=start_index + 1):
        print(f"✏️ Summarizing paper {i}/{len(data)}: {paper.get('Title', 'No Title')}")
        try:
            prompt = prompts.json_summarize_prompt(json.dumps(paper, ensure_ascii=False, indent=2))
            result = call_api(prompt)

            result = result.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

            summarized_json = json.loads(result)

            summarized_json = flatten_fields(summarized_json)

            summarized_data.append(summarized_json)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summarized_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"❌ Error summarizing paper {i}: {e}")

    print(f"✅ Summarized results saved to {output_path}")