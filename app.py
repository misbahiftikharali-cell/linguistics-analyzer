import streamlit as st
import json
from file_parser import parse_file
from pipeline import run_full_pipeline
from report_generator import generate_docx_report

st.set_page_config(
    page_title="PMDD Forensic Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional, high-precision forensic look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    .highlight {
        background-color: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid rgba(88, 166, 255, 0.3);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }
    
    .forensic-card {
        background-color: #161b22;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        color: #8b949e;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }
    
    .metric-value {
        color: #58a6ff;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Ensure all markdown and write text is visible */
    .stMarkdown, p, span, label {
        color: #c9d1d9 !important;
    }
    
    h1, h2, h3, h4, h5 {
        color: #f0f6fc !important;
        font-weight: 700 !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0d1117;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 6px 6px 0 0;
        padding: 12px 24px;
        color: #8b949e;
        border: 1px solid #30363d;
        border-bottom: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #21262d !important;
        color: #58a6ff !important;
        border-bottom: 3px solid #58a6ff !important;
    }
</style>
""", unsafe_allow_html=True)

def render_highlighted_text(text):
    """Replaces <<text>> with highlighted HTML span"""
    if not isinstance(text, str):
        return str(text)
    import re
    # Match << >> and replace with styled span
    formatted_text = re.sub(r'<<(.*?)>>', r'<span class="highlight">\1</span>', text)
    return formatted_text

st.markdown("# 🧠 Pragmatic Meaning Drift Detector (PMDD)")
st.markdown("### *Forensic Linguistic Evidence Synthesizer*")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
    st.header("Pipeline Control")
    uploaded_file = st.file_uploader("Upload Corpus (.txt, .csv, .json, .pdf)", type=['txt', 'csv', 'json', 'pdf'])
    
    st.markdown("---")
    st.markdown("**Theoretical Frameworks:**")
    st.caption("• Fairclough (1992) - CDA")
    st.caption("• Halliday (1978) - SFL")
    st.caption("• Sinclair (1991) - Corpus Stats")
    st.caption("• Lyons (1977) - Semantics")
    
    start_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

if start_analysis and uploaded_file is not None:
    text_content = parse_file(uploaded_file)
    
    if text_content.startswith("Error"):
        st.error(text_content)
    else:
        # Professional Pipeline Execution
        with st.status("Initializing Forensic Agents...", expanded=True) as status:
            def update_progress(msg):
                status.update(label=msg)
            
            results = run_full_pipeline(text_content, progress_callback=update_progress)
            status.update(label="✅ Analysis Complete", state="complete", expanded=False)
            
        st.markdown("---")
        
        # Check for any API or processing errors in the results
        api_error = None
        for agent_name in ["Agent1", "Agent2", "Agent3", "Agent4", "Agent5"]:
            agent_res = results.get(agent_name)
            if isinstance(agent_res, dict) and "error" in agent_res:
                api_error = agent_res["error"]
                break
        
        if api_error:
            st.error(f"🚨 **Pipeline Execution Error:** {api_error}")
            if "API key" in api_error or "reported as leaked" in api_error or "403" in api_error or "401" in api_error or "API Key" in api_error:
                st.warning("💡 **Linguistic Analyzer API Key Issue:**\n\n"
                           "Your Google Gemini API Key is missing, invalid, or has been **revoked by Google** because it was exposed in a public repository (e.g. uploaded to GitHub).\n\n"
                           "**How to fix this:**\n"
                           "1. Go to [Google AI Studio](https://aistudio.google.com/) and create a new Gemini API Key.\n"
                           "2. Open your Streamlit dashboard at [share.streamlit.io](https://share.streamlit.io/).\n"
                           "3. Go to your app's **Settings** -> **Secrets** and set/update your new key:\n"
                           "   ```toml\n"
                           "   GEMINI_API_KEY = \"your-new-gemini-api-key\"\n"
                           "   ```\n"
                           "4. Click **Save** and reboot/refresh the app.\n\n"
                           "*Note: To run it locally, create a file named `.env` in the project root directory with: `GEMINI_API_KEY=your-new-gemini-api-key`.*")
            st.stop()
        
        # ==========================================
        # SUMMARY DASHBOARD (Agent 5)
        # ==========================================
        st.header("📊 Synthesis Dashboard")
        a5 = results.get("Agent5", {})
        exec_summary = a5.get("executive_summary", {})
        drift_out = a5.get("drift_output", {})
        
        col_sum, col_drift = st.columns([2, 1])
        
        with col_sum:
            st.markdown('<div class="forensic-card">', unsafe_allow_html=True)
            st.markdown(f"**Executive Summary:**")
            st.markdown(render_highlighted_text(exec_summary.get('content', 'No summary generated.')), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_drift:
            st.markdown('<div class="forensic-card">', unsafe_allow_html=True)
            st.markdown("**⚖️ Drift Assessment**")
            drift_status = drift_out.get("status", "No drift data available.")
            if "Drift scores not statistically computed" in drift_status:
                st.warning(drift_status)
            else:
                st.success(drift_status)
                if drift_out.get("values"):
                    st.json(drift_out.get("values"))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ==========================================
        # THEORETICAL FRAMEWORK MAP
        # ==========================================
        st.header("🔬 Theoretical Framework Map")
        tcol1, tcol2, tcol3 = st.columns(3)
        
        with tcol1:
            st.info("**A1: Sinclair (1991)**\n\n*Purpose:* Empirical segmentation & tokenization to ensure count-verifiable data.")
            st.info("**A2: Pragmatics (Austin, Searle, Grice, B&L)**\n\n*Purpose:* Speech Act Theory, Maxim Violations, and Politeness strategies.")
            
        with tcol2:
            st.info("**A3: Semantics (Lyons, Halliday)**\n\n*Purpose:* Semantic Field Theory and Register Map (Field/Tenor/Mode).")
            st.info("**A4: Corpus Stats (Sinclair, Scott)**\n\n*Purpose:* Frequency analysis, Collocation, and Keyness variations.")
            
        with tcol3:
            st.info("**A5: Orchestration (Fairclough)**\n\n*Purpose:* Critical Discourse Analysis (CDA) synthesis and drift interpretation.")

        st.markdown("---")
        
        # ==========================================
        # INTEGRATED EVIDENCE REPORT
        # ==========================================
        st.header("🔎 Integrated Evidence Report")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "A1: Corpus Structuring", 
            "A2: Pragmatic Evidence", 
            "A3: Semantic Evidence", 
            "A4: Statistical Evidence",
            "A5: Forensic Synthesis"
        ])
        
        with tab1:
            st.subheader("Agent 1: Corpus Preprocessing (John Sinclair)")
            a1 = results.get("Agent1", {})
            segments = a1.get("segments", [])
            info = a1.get("corpus_info", {})
            
            st.markdown("""
            **Tagging Logic:** 
            Text is tagged based on Sinclair's principles of 'Ecology of Language'. Every punctuation mark and word is isolated to allow for precise quantitative tracking.
            """)
            
            if segments:
                st.success(f"✅ Corpus Validated: {len(segments)} segments, {info.get('total_tokens', 0)} tokens.")
                
                # Show as an integrated ledger instead of segments
                ledger_data = []
                for seg in segments:
                    ledger_data.append({
                        "ID": seg.get('id', ''),
                        "Tagged Text": f"<< {seg.get('text', '')} >>",
                        "Word Count": seg.get('word_count', 0),
                        "Tokens": ", ".join(seg.get('tokens', []))
                    })
                st.table(ledger_data)
                
                st.markdown("### Agent 1 Interpretation")
                st.write("The corpus has been normalized and structured into empirical units. This ensures that downstream agents are analyzing consistent linguistic segments without metadata noise.")
            else:
                st.warning("No segments generated.")
        
        with tab2:
            st.subheader("Agent 2: Pragmatic Evidence Ledger")
            a2 = results.get("Agent2", [])
            segments_a2 = a2 if isinstance(a2, list) else a2.get("segments", [])
            
            # --- THEORY 1: Speech Act Theory (Austin/Searle) ---
            st.markdown("#### 1️⃣ Speech Act Theory (Austin 1962 / Searle 1969)")
            st.markdown("**Purpose:** To identify the 'illocutionary force' (the action) performed by the utterance.")
            a2_sa_ledger = []
            for seg in segments_a2:
                basis = f"**Basis:** *{', '.join(seg.get('trigger_phrases', []))}*" if seg.get('trigger_phrases') else ""
                a2_sa_ledger.append({
                    "ID": seg.get('segment_id', ''),
                    "Tagged Text": f"<< {seg.get('text', '')} >>",
                    "Speech Act": seg.get('speech_act', 'N/A'),
                    "Forensic Explanation (Why/How)": f"{basis} \n\n {seg.get('speech_act_explanation', seg.get('explanation', 'N/A'))}"
                })
            st.table(a2_sa_ledger)
            
            # Show Theory Rules at the end of theory results
            if segments_a2 and segments_a2[0].get('speech_act_rules'):
                with st.expander("⚖️ Speech Act Theory: Rules & Application Logic", expanded=False):
                    st.markdown(f"**Rules Applied:**\n{segments_a2[0].get('speech_act_rules')}")
                    st.markdown(f"**Application Logic:**\n{segments_a2[0].get('speech_act_application')}")
            
            # --- THEORY 2: Cooperative Principle (Grice 1975) ---
            st.markdown("#### 2️⃣ Cooperative Principle & Maxims (Grice 1975)")
            st.markdown("**Purpose:** To detect violations that lead to non-literal meaning (implicatures).")
            a2_grice_ledger = []
            for seg in segments_a2:
                violations = seg.get('maxim_violations', [])
                if violations:
                    a2_grice_ledger.append({
                        "ID": seg.get('segment_id', ''),
                        "Tagged Text": f"<< {seg.get('text', '')} >>",
                        "Violation": ", ".join(violations),
                        "Forensic Explanation": seg.get('maxim_explanation', 'N/A')
                    })
            if a2_grice_ledger:
                st.table(a2_grice_ledger)
                if segments_a2 and segments_a2[0].get('maxim_rules'):
                    with st.expander("⚖️ Gricean Maxims: Rules & Application Logic", expanded=False):
                        st.markdown(f"**Rules Applied:**\n{segments_a2[0].get('maxim_rules')}")
                        st.markdown(f"**Application Logic:**\n{segments_a2[0].get('maxim_application')}")
            else:
                st.write("No significant Gricean violations detected in this corpus.")

            # --- THEORY 3: Politeness Theory (Brown & Levinson 1987) ---
            st.markdown("#### 3️⃣ Politeness & Face Theory (Brown & Levinson 1987)")
            st.markdown("**Purpose:** To analyze social distance and 'Face Threatening Acts' (FTAs).")
            a2_face_ledger = []
            for seg in segments_a2:
                score = seg.get('politeness_score', 3)
                a2_face_ledger.append({
                    "ID": seg.get('segment_id', ''),
                    "Tagged Text": f"<< {seg.get('text', '')} >>",
                    "Politeness Level": f"{score}/5",
                    "Forensic Explanation": seg.get('politeness_explanation', 'N/A')
                })
            st.table(a2_face_ledger)
            if segments_a2 and segments_a2[0].get('politeness_rules'):
                with st.expander("⚖️ Politeness Theory: Rules & Application Logic", expanded=False):
                    st.markdown(f"**Rules Applied:**\n{segments_a2[0].get('politeness_rules')}")
                    st.markdown(f"**Application Logic:**\n{segments_a2[0].get('politeness_application')}")
            
            st.markdown("---")
            st.markdown("### Agent 2 Integrated Interpretation")
            st.info("By layering these three theories, Agent 2 concludes that the discourse follows a specific pragmatic trajectory, often moving from neutral assertions to strategic violations of clarity.")


        
        with tab3:
            st.subheader("Agent 3: Semantic & Register Evidence Ledger")
            a3_list = results.get("Agent3", [])
            if not isinstance(a3_list, list): a3_list = [a3_list] if a3_list else []
            
            # --- THEORY 1: Semantic Field Theory (Lyons 1977) ---
            st.markdown("#### 1️⃣ Semantic Field Theory (Lyons 1977)")
            st.markdown("**Purpose:** To map the conceptual domains and 'Ideological Prosody' of the text.")
            a3_sem_ledger = []
            for a3 in a3_list:
                sa = a3.get("semantic_analysis", {})
                a3_sem_ledger.append({
                    "ID": a3.get('segment_id', 'N/A'),
                    "Tagged Text": f"<< {a3.get('text', 'N/A')} >>",
                    "Dominant Fields": ", ".join(sa.get('dominant_fields', [])),
                    "Why/How Explanation": sa.get("field_reasoning", "N/A")
                })
            st.table(a3_sem_ledger)
            if a3_list and a3_list[0].get("semantic_analysis", {}).get("theory_rules"):
                with st.expander("⚖️ Semantic Field Theory: Rules & Application Logic", expanded=False):
                    st.markdown(f"**Rules Applied:**\n{a3_list[0]['semantic_analysis'].get('theory_rules')}")
                    st.markdown(f"**Application Logic:**\n{a3_list[0]['semantic_analysis'].get('how_applied')}")

            # --- THEORY 2: Systemic Functional Linguistics (Halliday 1978) ---
            st.markdown("#### 2️⃣ Register Analysis - SFL Framework (Halliday 1978)")
            st.markdown("**Purpose:** To analyze the 'Field' (what is happening), 'Tenor' (who is involved), and 'Mode' (the role of language).")
            a3_reg_ledger = []
            for a3 in a3_list:
                ra = a3.get("register_analysis", {})
                a3_reg_ledger.append({
                    "ID": a3.get('segment_id', 'N/A'),
                    "Tagged Text": f"<< {a3.get('text', 'N/A')} >>",
                    "Register": f"{ra.get('primary_register', 'N/A')}",
                    "Field/Tenor/Mode": f"{ra.get('field', 'N/A')} / {ra.get('tenor', 'N/A')} / {ra.get('mode', 'N/A')}",
                    "Forensic Explanation": ra.get("reasoning", "N/A")
                })
            st.table(a3_reg_ledger)
            if a3_list and a3_list[0].get("register_analysis", {}).get("theory_rules"):
                with st.expander("⚖️ Register Analysis (SFL): Rules & Application Logic", expanded=False):
                    st.markdown(f"**Rules Applied:**\n{a3_list[0]['register_analysis'].get('theory_rules')}")
                    st.markdown(f"**Application Logic:**\n{a3_list[0]['register_analysis'].get('how_applied')}")
            
            st.markdown("---")
            st.markdown("### Agent 3 Integrated Interpretation")
            st.write("By combining Semantic Fields and Register analysis, Agent 3 detects whether the speaker is 'borrowing' registers from other domains (e.g., using military language in a political context) to create semantic drift.")
        with tab4:
            st.subheader("Agent 4: Statistical Corpus Evidence")
            a4 = results.get("Agent4", {})
            stats = a4.get("corpus_statistics", {})
            if isinstance(stats, dict):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Tokens", stats.get("total_tokens", 0))
                c2.metric("Total Types", stats.get("total_types", 0))
                c3.metric("TTR", f"{stats.get('type_token_ratio', 0.0):.4f}")
                c4.metric("Lexical Density", f"{stats.get('lexical_density', 0.0):.2f}")
            
            st.divider()
            
            # --- THEORY 1: Frequency Analysis (Sinclair 1991) ---
            st.markdown("#### 1️⃣ Frequency & Distribution Analysis (Sinclair 1991)")
            st.markdown("**Purpose:** To identify quantitatively prominent terms in the discourse.")
            a4_ledger_freq = []
            freq_data = a4.get("frequency_analysis", [])
            for item in freq_data:
                a4_ledger_freq.append({
                    "Word Tag": f"<< {item.get('word')} >>",
                    "Frequency": item.get('frequency'),
                    "Pattern": item.get('distribution_pattern'),
                    "Forensic Explanation": item.get('interpretation')
                })
            st.table(a4_ledger_freq)
            if freq_data and freq_data[0].get('theory_rules'):
                with st.expander("⚖️ Frequency Analysis: Rules & Application Logic", expanded=False):
                    st.markdown(f"**Rules Applied:**\n{freq_data[0].get('theory_rules')}")
                    st.markdown(f"**Application Logic:**\n{freq_data[0].get('how_applied')}")

            # --- THEORY 2: Keyness & Pattern Analysis (Scott 1997) ---
            st.markdown("#### 2️⃣ Keyness & Lexical Patterns (Scott 1997)")
            st.markdown("**Purpose:** To detect 'Keywords' that are statistically significant to the corpus's drift.")
            a4_ledger_key = []
            keyness = a4.get("keyness_analysis", []) # Agent 4 provides this if sample size is sufficient
            for k in keyness:
                a4_ledger_key.append({
                    "Keyword Tag": f"<< {k.get('keyword', k.get('word'))} >>",
                    "Keyness Score": k.get('keyness_score', 'N/A'),
                    "Significance": k.get('significance', 'N/A'),
                    "Forensic Explanation": k.get('drift_potential', 'N/A')
                })
            if a4_ledger_key:
                st.table(a4_ledger_key)
                if keyness and keyness[0].get('theory_rules'):
                    with st.expander("⚖️ Keyness Analysis: Rules & Application Logic", expanded=False):
                        st.markdown(f"**Rules Applied:**\n{keyness[0].get('theory_rules')}")
                        st.markdown(f"**Application Logic:**\n{keyness[0].get('how_applied')}")
            else:
                st.write("No statistically significant 'Keywords' (Scott 1997) detected in this specific sample.")
            
            st.markdown("---")
            st.markdown("### Agent 4 Interpretation")
            profile = a4.get("corpus_discourse_profile", {})
            st.success(profile.get("overall_quantitative_interpretation", "Quantitative analysis provides a baseline for identifying 'Keyword' prominence which supports claims of drift."))

        with tab5:
            st.subheader("Agent 5: Integrated Forensic Synthesis")
            st.markdown("""
            **Tagging Logic:** 
            Synthesis is tagged based on **Fairclough's CDA (Critical Discourse Analysis)**. 
            Cross-agent patterns are tagged as 'Linguistic Drift' if they appear consistently across multiple layers.
            """)
            
            a5 = results.get("Agent5", {})
            
            # 1. Quality Control
            qc = a5.get("quality_control", {})
            if qc.get("reanalysis_required"):
                st.error(f"🚨 Quality Alert: {qc.get('quality_summary')}")
            else:
                st.success("✅ Forensic Quality Check Passed")

            st.divider()

            # 2. Synthesis Ledger
            st.markdown("#### 📑 Cross-Agent Evidence Ledger")
            synth_data = []
            layers = [
                ("Pragmatic", a5.get("pragmatic_findings", {})),
                ("Semantic", a5.get("semantic_findings", {})),
                ("Register", a5.get("register_findings", {})),
                ("Statistical", a5.get("quantitative_findings", {}))
            ]
            for layer_name, layer_data in layers:
                finding = layer_data.get("interpretation", layer_data.get("statistical_interpretation", "N/A"))
                rules = layer_data.get("theory_rules_summary", "N/A")
                logic = layer_data.get("application_logic_summary", "N/A")
                synth_data.append({
                    "Layer": layer_name,
                    "Finding": finding,
                    "Rules Applied": rules,
                    "Application Logic": logic
                })
            st.table(synth_data)
            
            st.divider()

            # 3. Final Forensic Interpretation
            st.markdown("#### 🌐 Final Linguistic Interpretation")
            conclusion = a5.get("final_conclusion", {})
            st.info(conclusion.get("overall_interpretation", "No final interpretation generated."))
            
            st.markdown("### Agent 5 Final Explanation")
            st.write("Agent 5 has integrated all forensic layers to determine if linguistic drift is present. By combining pragmatic intent with semantic framing and statistical frequency, we can provide a high-confidence assessment of how meaning has evolved across the corpus.")
            st.warning(f"**Caution:** {conclusion.get('recommended_caution', '')}")
        
        st.markdown("---")
        
        # ==========================================
        # DOWNLOADABLE JSON
        # ==========================================
        st.header("💾 Export Findings")
        col_json, col_word = st.columns(2)
        
        with col_json:
            full_json = json.dumps(results, indent=2)
            st.download_button(
                label="📥 Download JSON Report",
                data=full_json,
                file_name="pmdd_forensic_report.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_word:
            docx_file = generate_docx_report(results)
            st.download_button(
                label="📥 Download Word Report (.docx)",
                data=docx_file,
                file_name="pmdd_forensic_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        
elif start_analysis and uploaded_file is None:
    st.warning("⚠️ Please upload a corpus file to begin investigation.")

