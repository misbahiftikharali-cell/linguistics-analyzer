import json
import re
from llm_utils import call_openai_json

AGENT1_PROMPT = """You are a Corpus Preprocessor & Segmenter Agent based on corpus linguistics methodology (Sinclair framework) and computational NLP preprocessing standards.

Your task is to transform raw text into a fully validated, self-consistent corpus.

You MUST NOT produce output unless all validation checks pass internally.

---

# 🔴 1. CORE PRINCIPLE (Sinclair)

All output must be:

* empirical
* reproducible
* count-verifiable
* structurally consistent

No intuition-based assumptions are allowed.

---

# 🔵 2. PREPROCESSING RULES

* Remove noise (HTML, scripts, metadata)
* Normalize whitespace
* Preserve punctuation
* Convert text to UTF-8

---

# 🟢 3. SEGMENTATION RULES

* Split into sentences using: ., !, ?
* Do NOT split abbreviations (Dr., etc.)
* Preserve order strictly

---

# 🟣 4. TOKENIZATION RULES (STRICT)

For each sentence:

* Token = word OR punctuation
* Separate punctuation into individual tokens
* Keep quotes as tokens
* Maintain consistency across all segments

---

# 🟡 5. WORD COUNT RULE (CRITICAL FIX)

You MUST define and enforce:

word_count = number of tokens EXCLUDING:

* punctuation marks
* quotes (“ ”)
* commas (,)
* full stops (.)

👉 ONLY alphabetic/alphanumeric words count

If mismatch found → recalculate before output

---

# ⚙️ 6. VALIDATION ENGINE (MANDATORY)

Before final output, perform:

### STEP 1: Segment Check

* total_sentences = number of segments
* MUST match exactly

### STEP 2: Token Check

* sum(tokens in all segments) = total_tokens
* MUST match

### STEP 3: Word Count Check

For each segment:

* recompute word_count from tokens
* if mismatch → FIX automatically

### STEP 4: Consistency Check

* no missing segments
* no duplicate positions
* order preserved

❗ If ANY check fails → do NOT output until corrected

---

# 🧾 7. OUTPUT FORMAT (STRICT JSON ONLY)

{
"corpus_info": {
"total_tokens": number,
"total_sentences": number
},
"segments": [
{
"id": integer,
"position": integer,
"text": "string",
"word_count": integer,
"tokens": ["string"]
}
]
}

---

# 🧠 8. FINAL RULE (SELF-CORRECTION LOOP)

If any inconsistency is detected:

* recompute tokens
* recompute word_count
* update corpus_info
* revalidate again

Output only when system is fully consistent.

---

# 🚨 9. NO-GO CONDITIONS

Do NOT output if:

* counts are inconsistent
* segmentation mismatch exists
* word_count not derivable from tokens
* structure is incomplete

INPUT TEXT:
{TEXT}
"""

import re

def run_agent1(text: str, progress_callback=None) -> dict:
    print("Running Agent 1 (Corpus Preprocessor)...")
    
    # Chunking logic for large text
    # Chunking logic for large text
    CHUNK_SIZE = 5000 
    
    if len(text) <= CHUNK_SIZE:
        prompt = AGENT1_PROMPT.replace("{TEXT}", text)
        result = call_openai_json(prompt)
    else:
        print(f"Large text detected ({len(text)} chars). Processing in chunks...")
        # Split by punctuation to avoid cutting mid-sentence
        sentences_raw = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = ""
        
        for s in sentences_raw:
            if len(current_chunk) + len(s) < CHUNK_SIZE:
                current_chunk += s + " "
            else:
                if current_chunk: chunks.append(current_chunk.strip())
                current_chunk = s + " "
                # Handle edge case where a single sentence is larger than CHUNK_SIZE
                while len(current_chunk) > CHUNK_SIZE:
                    chunks.append(current_chunk[:CHUNK_SIZE])
                    current_chunk = current_chunk[CHUNK_SIZE:]
                    
        if current_chunk: chunks.append(current_chunk.strip())
        
        all_segments = []
        total_tokens = 0
        
        if progress_callback: progress_callback(f"Agent 1: Processing {len(chunks)} chunks in parallel...")
        
        for i, chunk in enumerate(chunks):
            msg = f"Agent 1: Processing chunk {i+1}/{len(chunks)}..."
            print(msg)
            # Removed progress_callback(msg) from here to avoid NoSessionContext
            
            prompt = AGENT1_PROMPT.replace("{TEXT}", chunk)
            chunk_result = call_openai_json(prompt)
            
            if "segments" in chunk_result:
                all_segments.extend(chunk_result["segments"])
            if "corpus_info" in chunk_result:
                total_tokens += chunk_result["corpus_info"].get("total_tokens", 0)
        
        # Re-index segments for global consistency
        for i, seg in enumerate(all_segments):
            seg["id"] = i
            seg["position"] = i
            
        result = {
            "corpus_info": {
                "total_tokens": total_tokens,
                "total_sentences": len(all_segments)
            },
            "segments": all_segments
        }

    # Programmatic self-correction for exact word count
    if "segments" in result:
        for seg in result["segments"]:
            tokens = seg.get("tokens", [])
            # A token counts as a word if it contains at least one alphanumeric character
            actual_word_count = sum(1 for t in tokens if re.search(r'[a-zA-Z0-9]', t))
            seg["word_count"] = actual_word_count
            
    return result
