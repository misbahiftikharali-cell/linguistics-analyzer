import json
from llm_utils import call_openai_json

AGENT2_PROMPT = """You are Agent 02: Pragmatic Analyzer.

You will receive input from Agent 01 (Corpus Preprocessor & Segmenter).

Your task is to analyze EACH segment and produce enriched pragmatic annotations based on:
- Speech Act Theory (Austin 1962; Searle 1969)
- Grice’s Cooperative Principle (1975)
- Politeness Theory (Brown & Levinson 1987)

-------------------------------------
INPUT FORMAT (FROM AGENT 01)
-------------------------------------
Example:
Seg 0 (Pos: 0, Words: 14): In recent years, the idea of “community engagement” has become central to political discourse.
Tokens: [...]

Seg 1 (Pos: 1, Words: 15): Governments now claim that they will “work closely with citizens” to ensure transparency.
Tokens: [...]

YOUR TASK
-------------------------------------

1. Extract EACH segment:
   - segment_id = Seg number (e.g., "Seg 0")
   - text = sentence after colon

2. Ignore:
   - Tokens
   - Statistics
   - Metadata

-------------------------------------
ANALYSIS STEPS
-------------------------------------

For EACH segment, perform the following steps:

-------------------------------------
STEP 1: SPEECH ACT (MANDATORY)
-------------------------------------
Classify ONE dominant speech act:

- Assertive → statement, description
- Directive → request, command, suggestion
- Commissive → promise, commitment
- Expressive → emotion (thanks, apology)
- Declaration → institutional act

-------------------------------------
STEP 2: MAXIM VIOLATIONS
-------------------------------------
Detect violations of Grice’s maxims (Quantity, Quality, Relation, Manner). Return as array.

-------------------------------------
STEP 3: IMPLICATURE
-------------------------------------
- Conversational → due to maxim violation
- Conventional → due to specific words
- None → if no implied meaning

-------------------------------------
STEP 4: POLITENESS SCORE (1-5)
-------------------------------------
Assign score (1–5):
1 → Very impolite/aggressive
3 → Neutral/Direct
5 → Very polite/Highly indirect

-------------------------------------
STEP 5: FORENSIC EVIDENCE & TRACEABILITY
-------------------------------------
- **evidence**: An object containing speech-act specific markers (e.g., directive_marker, assertive_marker, etc.), boolean 'indirectness', and 'face_saving_strategy'.
- **evidence_span**: The exact substring from the segment text that supports the analysis.
- **trigger_phrases**: A list of specific words or phrases that triggered the classification.
- **confidence_score**: A value from 0.0 to 1.0 representing your certainty.
- **explanation**: A clear forensic explanation of the pragmatic logic used.

-------------------------------------
OUTPUT FORMAT (STRICT)
-------------------------------------

Return JSON array ONLY:

[
  {
    "segment_id": 1,
    "text": "original text here",
    "speech_act": "Directive",
    "speech_act_explanation": "Why this speech act?",
    "speech_act_rules": "Define the rules of Speech Act Theory used (e.g., Searle's taxonomy).",
    "speech_act_application": "How the rules were applied to this specific segment.",
    "maxim_violations": ["Quality"],
    "maxim_explanation": "Why this violation?",
    "maxim_rules": "Define the Gricean Maxim rules used.",
    "maxim_application": "How the rules were applied to this specific segment.",
    "implicature_type": "Conversational",
    "politeness_score": 5,
    "politeness_explanation": "Why this score?",
    "politeness_rules": "Define the Politeness Theory rules used (e.g., Face Saving).",
    "politeness_application": "How the rules were applied to this specific segment.",
    "evidence": {
      "directive_marker": "Could you",
      "indirectness": true,
      "face_saving_strategy": "negative politeness"
    },
    "evidence_span": "the part of the text",
    "trigger_phrases": ["phrase1", "phrase2"],
    "confidence_score": 0.95,
    "explanation": "Overall forensic synthesis...",
    "pragmatic_ambiguity": false,
    "negative_analysis": {
      "limitations": "...",
      "alternative_interpretation": "..."
    }
  }
]

-------------------------------------
IMPORTANT RULES
-------------------------------------
- DO NOT skip any segment.
- DO NOT change segment_id.
- ALWAYS include original text.
- ONLY return JSON array.
- Politeness score is 1-5.
- Evidence markers in the "evidence" object should adapt to the speech act (e.g., "assertive_marker" for Assertives).

INPUT DATA:
{TEXT}
"""

def run_agent2(text: str, progress_callback=None):
    print("Running Agent 2 (Pragmatic Analyzer)...")
    
    # Robust Input Handling:
    # If the input is the JSON output from Agent 1, we extract the segments
    segments = []
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "segments" in data:
            segments = data["segments"]
    except (json.JSONDecodeError, TypeError):
        # Fallback if text is not JSON (though Agent 2 expects Agent 1 output)
        return {"error": "Invalid input format for Agent 2"}

    if not segments:
        return []

    # Parallel Batch Processing logic
    BATCH_SIZE = 15
    all_results = []
    
    from concurrent.futures import ThreadPoolExecutor
    
    def process_batch(batch_idx, batch):
        batch_num = batch_idx + 1
        total_batches = (len(segments)-1)//BATCH_SIZE + 1
        msg = f"Agent 2: Processing batch {batch_num}/{total_batches}..."
        print(msg)
        # progress_callback(msg) removed from here for thread-safety
        
        formatted_batch = ""
        for seg in batch:
            seg_id = seg.get("id", "0")
            pos = seg.get("position", 0)
            words = seg.get("word_count", 0)
            txt = seg.get("text", "")
            tokens = seg.get("tokens", [])
            formatted_batch += f"Seg {seg_id} (Pos: {pos}, Words: {words}): {txt}\n"
            formatted_batch += f"Tokens: {json.dumps(tokens)}\n\n"
            
        prompt = AGENT2_PROMPT.replace("{TEXT}", formatted_batch)
        return call_openai_json(prompt)

    batches = [segments[i:i + BATCH_SIZE] for i in range(0, len(segments), BATCH_SIZE)]
    
    if progress_callback: progress_callback(f"Agent 2: Analyzing {len(batches)} batches in parallel...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        batch_results = list(executor.map(lambda x: process_batch(x[0], x[1]), enumerate(batches)))
        
    for batch_result in batch_results:
        if isinstance(batch_result, list):
            all_results.extend(batch_result)
        elif isinstance(batch_result, dict) and "segments" in batch_result:
            all_results.extend(batch_result["segments"])
            
    return all_results


