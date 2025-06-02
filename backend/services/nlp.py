from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
ner = pipeline("ner", grouped_entities=True)
import re

# Load the summarization model (use a stronger model if you have enough RAM)
summarizer = pipeline("summarization", model="google/flan-t5-large")
# For legal Q&A, you can also load a Q&A model:
qa_pipeline = pipeline("question-answering", model="nlpaueb/legal-bert-base-uncased")

def analyze_text(text):
    # Example: Extract entities or keywords using summarizer/other pipeline if needed
    # For now, just return the summary and entities as a demo
    summary = summarize_text(text)
    return {
        "summary": summary,
        # You can add more NLP analysis here in the future
    }

def summarize_text(text):
    # Use Hugging Face summarizer
    result = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return result[0]['summary_text']

def answer_question(question, context):
    # Use Hugging Face legal Q&A pipeline
    result = qa_pipeline(question=question, context=context)
    return result['answer']

CLAUSE_KEYWORDS = [
    "indemnity", "termination", "confidentiality", "dispute resolution",
    "governing law", "liability", "force majeure", "assignment"
]

def extract_clauses(text):
    clauses = {}
    for keyword in CLAUSE_KEYWORDS:
        # This is a simple pattern; for real apps, use ML or more advanced regex
        pattern = re.compile(rf"({keyword}.*?)(?=\n[A-Z][a-z]+|\Z)", re.IGNORECASE | re.DOTALL)
        matches = pattern.findall(text)
        if matches:
            clauses[keyword] = matches
    return clauses

def detect_risks(clauses):
    risks = []
    required = ["indemnity", "termination", "confidentiality"]
    for req in required:
        if req not in clauses:
            risks.append(f"Missing critical clause: {req.title()}")
    # Add more advanced checks as needed
    return risks

def extract_entities(text):
    return ner(text)

def compare_to_template(clauses, template_clauses):
    deviations = {}
    for key, standard_text in template_clauses.items():
        if key in clauses and clauses[key][0] != standard_text:
            deviations[key] = {
                "found": clauses[key][0],
                "expected": standard_text
            }
    return deviations

def risk_score(risks):
    return len(risks) * 10  # Example: each risk adds 10 points

def semantic_search(query, clause_texts):
    query_emb = semantic_model.encode(query, convert_to_tensor=True)
    clause_embs = semantic_model.encode(clause_texts, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_emb, clause_embs)[0]
    top_idx = scores.argmax().item()
    return clause_texts[top_idx], float(scores[top_idx])



