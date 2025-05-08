import api_calls as api
import dataManager

input_file = ""
output_file = ""
filtered_metadata_file = ""

if __name__ == "__main__":
	api.ris_filter()
	api.process_all_pdfs(input_file, output_file)
	api.summarize_json_results(input_file, output_file)
	dataManager.json_to_excel(output_file, "output/results.xlsx", dataManager.build_ris_metadata_map("input/My Library.ris"), "output/countries.json")
	api.filter_pdfs_with_criteria(input_file, output_file)
	dataManager.extract_filtered_metadata(input_file, output_file, filtered_metadata_file)
	dataManager.find_missing_titles(filtered_metadata_file, output_file)
	dataManager.compare_ris_files(filtered_metadata_file, "Second_Data/final_result.ris", "output")