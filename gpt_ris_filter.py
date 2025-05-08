import os
from openai import OpenAI
import dataManager
import prompts

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

model = "gpt-4.1-mini-2025-04-14"
temperature = 0.2
max_tokens = 10000
topic = "paper_filtering"
input_file = "output/gpt_filtered_metadata_v2.ris"
output_file = "output/gpt_filtered_titles_v2.txt"
filtered_metadata_file = "output/unmatched_titles.ris"

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

def main():
	papers = dataManager.parse_ris(input_file)
	batches = dataManager.batch_papers(papers)

	for i, batch in enumerate(batches):
		print(f"Processing batch {i+1}/{len(batches)}...")
		batch_text = dataManager.format_batch_for_prompt(batch)
		prompt = prompts.get_second_filter_prompt(batch_text)
		try:
			result = call_api(prompt)
			save_results(result)
		except Exception as e:
			print(f"Error on batch {i+1}: {e}")

if __name__ == "__main__":
	# main()
    dataManager.extract_filtered_metadata(input_file, "output/unmatched_titles.txt", filtered_metadata_file)
    # dataManager.find_missing_titles(filtered_metadata_file, output_file)
	# dataManager.compare_ris_files(filtered_metadata_file, "Second_Data/final_result.ris", "output")