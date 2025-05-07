import rispy

def ris_filter(entry):
	year = entry.get('year')
	if not year or not (2020 <= int(year) <= 2025):
		return False

	lang = entry.get('language', '').lower()
	if lang and 'english' not in lang:
		return False

	doc_type = entry.get('type_of_reference', '').lower()
	if doc_type != 'jour':
		return False

	title = entry.get('title', '').lower()
	abstract = entry.get('abstract', '').lower()
	keywords = ' '.join(entry.get('keywords', [])).lower()
	text = f"{title} {abstract} {keywords}"

	edu_terms = ['higher education', 'university', 'college']
	if not any(term in title or term in abstract for term in edu_terms):
		return False

	exclude_terms = ['k-12', 'corporate training', 'workplace training', 'vocational training']
	if any(term in text for term in exclude_terms):
		return False

	ai_terms = [
		'artificial intelligence', 'machine learning', 'deep learning',
		'natural language processing', 'neural networks', 'chatgpt', 'gpt-4', 'large language model',
		'transformer models', 'generative ai'
	]
	if not any(term in title or term in abstract for term in ai_terms):
		return False

	risk_terms = [
		'ethical', 'ethics', 'data privacy', 'privacy', 'bias', 'fairness', 'security',
		'trust', 'accountability', 'discrimination', 'social implications', 'ai safety', 'risk', "challenge",
		'problems', 'concerns', 'issues', 'limitations', 'vulnerabilities', 'threats', 'harms',
		'negative impact', 'adverse effects', 'unintended consequences', 'misuse', 'abuse', 'equity',
	]
	risk_matches = [term for term in risk_terms if term in text]
	if len(risk_matches) < 2:
		return False

	research_terms = [
		'empirical', 'experimental', 'observational', 'data analysis', 'survey', 'case study',
		'research', 'theoretical framework', 'methodology'
	]
	if not any(term in text for term in research_terms):
		return False

	exclude_research_terms = ['editorial', 'poster', 'brief', 'letter']
	if any(term in text for term in exclude_research_terms):
		return False

	return True
with open('Second_Data/my_library.ris', 'r', encoding='utf-8') as f:
	entries = rispy.load(f)

filtered = [e for e in entries if ris_filter(e)]

with open('Second_Data/resultv7.ris', 'w', encoding='utf-8') as f:
	rispy.dump(filtered, f)