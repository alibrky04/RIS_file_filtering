import rispy

def is_valid_entry(entry):
	# 1. Year filter
	year = entry.get('year')
	if not year or not (2020 <= int(year) <= 2025):
		return False

	# 2. Language filter
	lang = entry.get('language', '').lower()
	if lang and 'english' not in lang:
		return False

	# 3. Document type filter (case-insensitive)
	doc_type = entry.get('type_of_reference', '').lower()
	if doc_type != 'jour':
		return False

	# Combine abstract + keywords + title for text search
	text = ' '.join([
		entry.get('abstract', ''),
		' '.join(entry.get('keywords', [])),
		entry.get('title', '')
	]).lower()

	# 4. Subject context filter (broader terms)
	subject_terms = ['higher education', 'university', 'college', 'post-secondary', 'tertiary education', 'academic institutions', 'university education']
	if not any(term in text for term in subject_terms):
		return False

	exclude_terms = ['k-12', 'corporate training', 'workplace training', 'vocational training']
	if any(term in text for term in exclude_terms):
		return False

	# 5. AI focus (broader)
	ai_terms = [
		'artificial intelligence', 'machine learning', 'deep learning', 'neural networks', 'natural language processing',
		'chatbot', 'large language model', 'ai', 'computer vision', 'speech recognition', 'chat gpt', 'gemini', 'gpt-3', 'gpt-4', 
		'generative ai', 'language model', 'ai systems', 'artificial neural networks', 'reinforcement learning', 'openai', 'transformer models'
	]
	if not any(term in text for term in ai_terms):
		return False

	# 6. Risks & challenges (broader)
	risk_terms = [
		'ethical', 'ethics', 'data privacy', 'privacy', 'teacher resistance', 'bias', 'biased', 'fairness', 'data security', 'security', 
		'trust', 'responsibility', 'transparency', 'accountability', 'data governance', 'discrimination', 'algorithmic bias', 'misuse of ai', 
		'data breaches', 'informed consent', 'social implications', 'ai ethics', 'human rights', 'transparency in ai', 'ai safety'
	]
	if not any(term in text for term in risk_terms):
		return False

	# 7. Research type filter (Empirical and Theoretical)
	# Look for keywords related to empirical (e.g., experimental, observational) and theoretical research
	research_terms = ['experimental', 'observational', 'empirical', 'theoretical', 'study', 'research', 'data analysis', 'survey', 'experiment', 'case study', 'field study']
	if not any(term in text for term in research_terms):
		return False

	# Ensure that editorial, opinion, and poster articles are excluded
	#exclude_research_terms = ['editorial', 'poster', 'brief', 'letter']
	#if any(term in text for term in exclude_research_terms):
		#return False

	return True

with open('merge.ris', 'r', encoding='utf-8') as f:
	entries = rispy.load(f)

filtered = [e for e in entries if is_valid_entry(e)]

with open('resultv3.ris', 'w', encoding='utf-8') as f:
	rispy.dump(filtered, f)