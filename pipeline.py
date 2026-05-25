import json
from agent1_preprocessor import run_agent1
from agent2_pragmatic_analyzer import run_agent2
from agent3_semantic_analyzer import run_agent3
from agent4_corpus_statistician import run_agent4
from agent5_orchestrator import run_agent5

def run_full_pipeline(text: str, progress_callback=None):
    """
    Runs the text through all 5 PMDD agents sequentially.
    progress_callback is a function to update the UI on current step.
    """
    results = {}
    
    if progress_callback: progress_callback("Agent 1: Corpus Preprocessing...")
    results["Agent1"] = run_agent1(text, progress_callback=progress_callback)
    
    # Use Agent 1's segmented JSON as input for downstream agents
    segmented_json = json.dumps(results["Agent1"])
    
    if progress_callback: progress_callback("Agent 2: Pragmatic Analysis...")
    results["Agent2"] = run_agent2(segmented_json, progress_callback=progress_callback)
    
    if progress_callback: progress_callback("Agent 3: Semantic & Register Analysis...")
    results["Agent3"] = run_agent3(segmented_json, progress_callback=progress_callback)
    
    if progress_callback: progress_callback("Agent 4: Corpus Statistics...")
    results["Agent4"] = run_agent4(segmented_json)
    
    if progress_callback: progress_callback("Agent 5: Orchestrating & Synthesizing...")
    # Combine all results for Agent 5
    combined_inputs = {
        "Agent1": results["Agent1"],
        "Agent2": results["Agent2"],
        "Agent3": results["Agent3"],
        "Agent4": results["Agent4"]
    }
    results["Agent5"] = run_agent5(json.dumps(combined_inputs))
    
    if progress_callback: progress_callback("Pipeline Complete!")
    return results
