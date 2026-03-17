# # ============================================================
# # server.py
# # ============================================================

# from flask import Flask, request, jsonify, render_template
# from pipeline_runner import run_pipeline  # import the helper module

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/api/query", methods=["POST"])
# def api_query():
#     data = request.get_json(silent=True) or {}
#     query = (data.get("query") or "").strip()
#     if not query:
#         return jsonify({"error": "Missing 'query'"}), 400

#     print(f"🩺 Received query: {query}")
#     try:
#         results = run_pipeline(query)
#         return jsonify(results)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)
#################################################################################################
# from flask import Flask, request, jsonify, render_template
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# import torch, os

# # ============================================================
# # Load model once at startup
# # ============================================================

# print("🚀 Loading LLaMA-3 model ...")
# MODEL_ID = "./7B-v0.3" if os.path.isdir("./7B-v0.3") else "meta-llama/Meta-Llama-3-8B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# try:
#     bnb_config = BitsAndBytesConfig(
#         load_in_4bit=True,
#         bnb_4bit_quant_type="nf4",
#         bnb_4bit_compute_dtype=torch.float16,
#     )
# except Exception:
#     bnb_config = None

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_ID,
#     device_map="auto",
#     quantization_config=bnb_config,
#     dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
# )
# model.eval()
# print(f"✅ Model loaded: {MODEL_ID}")

# # ============================================================
# # Generation helper and pipeline
# # ============================================================

# @torch.inference_mode()
# def generate_response(prompt, max_tokens=500, temperature=0.7):
#     formatted = f"[INST] {prompt} [/INST]"
#     inputs = tokenizer(formatted, return_tensors="pt", padding=True,
#                        truncation=True, max_length=4096).to(model.device)
#     outputs = model.generate(**inputs, max_new_tokens=max_tokens,
#                              temperature=temperature, do_sample=True,
#                              pad_token_id=tokenizer.pad_token_id,
#                              eos_token_id=tokenizer.eos_token_id)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()

# DOMAINS = ["neurology", "general medicine", "ophthalmology", "dermatology", "psychology"]

# def run_pipeline(query):
#     # Step 1: detect domains
#     prompt1 = f"You are a medical query analyzer.\nQuery: '{query}'\nSelect 3–5 relevant domains from: {', '.join(DOMAINS)}."
#     analysis = generate_response(prompt1, max_tokens=80)
#     relevant = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5] or DOMAINS[:3]
#     # Steps 2–6: specialists
#     specialists = []
#     for d in relevant:
#         p = f"You are a {d} specialist doctor.\nQuery: '{query}'\nGive short bullet points for insights, causes, and recommendations."
#         specialists.append(f"{d.title()}:\n{generate_response(p, max_tokens=200)}")
#     # Step 7: summary
#     combined = "\n\n".join(specialists)
#     summary_prompt = f"You are a summarizer. Combine the following:\n{combined}\nFormat with Key Symptoms/Causes, Recommendations, and When to See a Doctor."
#     return generate_response(summary_prompt, max_tokens=300)

# # ============================================================
# # Flask routes
# # ============================================================

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/api/query", methods=["POST"])
# def api_query():
#     data = request.get_json()
#     query = (data.get("query") or "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400
#     print(f"🩺 Initial query: {query}")
#     summary = run_pipeline(query)
#     return jsonify({"query": query, "summary": summary})

# @app.route("/api/refine", methods=["POST"])
# def api_refine():
#     data = request.get_json()
#     query = (data.get("query") or "").strip()
#     details = (data.get("details") or "").strip()
#     if not query or not details:
#         return jsonify({"error": "Missing query or details"}), 400
#     updated_query = f"{query}. Additional details: {details}"
#     print(f"🔁 Refining query with new details.")
#     refined = run_pipeline(updated_query)
#     return jsonify({"query": updated_query, "summary": refined})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)
###############################################################################

# from flask import Flask, request, jsonify, render_template, session
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# import torch, os, uuid

# # ============================================================
# # 1️⃣ Flask setup with session key
# # ============================================================

# app = Flask(__name__)
# app.secret_key = "supersecretkey_change_this"  # used for secure sessions

# # ============================================================
# # 2️⃣ Load LLaMA-3 model once
# # ============================================================

# print("🚀 Loading LLaMA-3 model ...")
# MODEL_ID = "./7B-v0.3" if os.path.isdir("./7B-v0.3") else "meta-llama/Meta-Llama-3-8B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# try:
#     bnb_config = BitsAndBytesConfig(
#         load_in_4bit=True,
#         bnb_4bit_quant_type="nf4",
#         bnb_4bit_compute_dtype=torch.float16,
#     )
# except Exception:
#     bnb_config = None

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_ID,
#     device_map="auto",
#     quantization_config=bnb_config,
#     dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
# )
# model.eval()
# print(f"✅ Model loaded: {MODEL_ID}")

# # ============================================================
# # 3️⃣ Helper: generation + reasoning pipeline
# # ============================================================

# @torch.inference_mode()
# def generate_response(prompt, max_tokens=500, temperature=0.7):
#     formatted = f"[INST] {prompt} [/INST]"
#     inputs = tokenizer(formatted, return_tensors="pt", padding=True,
#                        truncation=True, max_length=4096).to(model.device)
#     outputs = model.generate(**inputs, max_new_tokens=max_tokens,
#                              temperature=temperature, do_sample=True,
#                              pad_token_id=tokenizer.pad_token_id,
#                              eos_token_id=tokenizer.eos_token_id)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()

# DOMAINS = ["neurology", "general medicine", "ophthalmology", "dermatology", "psychology"]

# def run_pipeline(query):
#     """Full medical reasoning pipeline returning summarized result."""
#     # Step 1: detect domains
#     prompt1 = f"You are a medical query analyzer.\nQuery: '{query}'\nSelect 3–5 relevant domains from: {', '.join(DOMAINS)}."
#     analysis = generate_response(prompt1, max_tokens=80)
#     relevant = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5] or DOMAINS[:3]

#     # Steps 2–6: specialists
#     specialists = []
#     for d in relevant:
#         p = f"You are a {d} specialist doctor.\nQuery: '{query}'\nGive short bullet points for insights, causes, and recommendations."
#         specialists.append(f"{d.title()}:\n{generate_response(p, max_tokens=200)}")

#     # Step 7: summary
#     combined = "\n\n".join(specialists)
#     summary_prompt = f"You are a summarizer. Combine the following:\n{combined}\nFormat with Key Symptoms/Causes, Recommendations, and When to See a Doctor."
#     return generate_response(summary_prompt, max_tokens=300)

# # ============================================================
# # 4️⃣  Routes
# # ============================================================

# @app.route("/")
# def home():
#     # Create a new session if not exists
#     if "user_id" not in session:
#         session["user_id"] = str(uuid.uuid4())
#         session["conversation"] = []  # store each query + result
#     return render_template("index.html")

# @app.route("/api/query", methods=["POST"])
# def api_query():
#     """Handle initial query"""
#     data = request.get_json()
#     query = (data.get("query") or "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     print(f"🩺 Initial query from {session['user_id']}: {query}")
#     summary = run_pipeline(query)

#     # Save to session
#     session["conversation"].append({
#         "query": query,
#         "response": summary
#     })
#     session.modified = True

#     return jsonify({
#         "query": query,
#         "summary": summary,
#         "conversation": session["conversation"]
#     })

# @app.route("/api/refine", methods=["POST"])
# def api_refine():
#     """Handle follow-up clarification"""
#     data = request.get_json()
#     details = (data.get("details") or "").strip()
#     if not details:
#         return jsonify({"error": "Missing details"}), 400

#     # Fetch last query from session
#     if "conversation" not in session or not session["conversation"]:
#         return jsonify({"error": "No active conversation."}), 400

#     last_query = session["conversation"][-1]["query"]
#     updated_query = f"{last_query}. Additional details: {details}"
#     print(f"🔁 Refining for user {session['user_id']} ...")

#     refined_summary = run_pipeline(updated_query)

#     # Append refinement
#     session["conversation"].append({
#         "query": updated_query,
#         "response": refined_summary
#     })
#     session.modified = True

#     return jsonify({
#         "query": updated_query,
#         "summary": refined_summary,
#         "conversation": session["conversation"]
#     })

# @app.route("/api/history", methods=["GET"])
# def api_history():
#     """Return full conversation history"""
#     history = session.get("conversation", [])
#     return jsonify(history)

# @app.route("/api/reset", methods=["POST"])
# def api_reset():
#     """Clear user session"""
#     session.pop("conversation", None)
#     return jsonify({"message": "Session reset successful."})

# # ============================================================
# # 5️⃣  Run
# # ============================================================

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)
###################################################################

#FINAL VERSION

# from flask import Flask, request, jsonify, render_template, session
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# import torch, os, uuid

# # ============================================================
# # 1️⃣ Flask setup and secret key for session persistence
# # ============================================================

# app = Flask(__name__)
# app.secret_key = "supersecretkey_change_this"  # replace with a random key in production

# # ============================================================
# # 2️⃣ Load LLaMA-3 model once globally
# # ============================================================

# print("🚀 Loading LLaMA-3 model ...")
# MODEL_ID = "./7B-v0.3" if os.path.isdir("./7B-v0.3") else "meta-llama/Meta-Llama-3-8B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# try:
#     bnb_config = BitsAndBytesConfig(
#         load_in_4bit=True,
#         bnb_4bit_quant_type="nf4",
#         bnb_4bit_compute_dtype=torch.float16,
#     )
# except Exception:
#     bnb_config = None

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_ID,
#     device_map="auto",
#     quantization_config=bnb_config,
#     dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
# )
# model.eval()
# print(f"✅ Model loaded: {MODEL_ID}")

# # ============================================================
# # 3️⃣ Before-request hook to ensure session always exists
# # ============================================================

# @app.before_request
# def ensure_session():
#     """Guarantees every request has a valid user_id and conversation."""
#     if "user_id" not in session:
#         session["user_id"] = str(uuid.uuid4())
#     if "conversation" not in session:
#         session["conversation"] = []

# # ============================================================
# # 4️⃣ Helper functions: generation and reasoning pipeline
# # ============================================================

# @torch.inference_mode()
# def generate_response(prompt, max_tokens=500, temperature=0.7):
#     formatted = f"[INST] {prompt} [/INST]"
#     inputs = tokenizer(formatted, return_tensors="pt", padding=True,
#                        truncation=True, max_length=4096).to(model.device)
#     outputs = model.generate(**inputs, max_new_tokens=max_tokens,
#                              temperature=temperature, do_sample=True,
#                              pad_token_id=tokenizer.pad_token_id,
#                              eos_token_id=tokenizer.eos_token_id)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()

# DOMAINS = ["neurology", "general medicine", "ophthalmology", "dermatology", "psychology"]

# def run_pipeline(query):
#     """Runs the full multi-specialist medical reasoning pipeline."""
#     # Step 1: detect domains
#     prompt1 = f"You are a medical query analyzer.\nQuery: '{query}'\nSelect 3–5 relevant domains from: {', '.join(DOMAINS)}."
#     analysis = generate_response(prompt1, max_tokens=80)
#     relevant = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5] or DOMAINS[:3]

#     # Steps 2–6: specialists
#     specialists = []
#     for d in relevant:
#         p = f"You are a {d} specialist doctor.\nQuery: '{query}'\nGive short bullet points for insights, causes, and recommendations."
#         specialists.append(f"{d.title()}:\n{generate_response(p, max_tokens=200)}")

#     # Step 7: final summary
#     combined = "\n\n".join(specialists)
#     summary_prompt = f"You are a summarizer. Combine the following:\n{combined}\nFormat with Key Symptoms/Causes, Recommendations, and When to See a Doctor."
#     return generate_response(summary_prompt, max_tokens=300)

# # ============================================================
# # 5️⃣ Routes
# # ============================================================

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/api/query", methods=["POST"])
# def api_query():
#     """Handles initial medical query."""
#     data = request.get_json()
#     query = (data.get("query") or "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     print(f"🩺 Initial query from {session['user_id']}: {query}")
#     summary = run_pipeline(query)

#     # Store in session
#     session["conversation"].append({
#         "query": query,
#         "response": summary
#     })
#     session.modified = True

#     return jsonify({
#         "query": query,
#         "summary": summary,
#         "conversation": session["conversation"]
#     })

# @app.route("/api/refine", methods=["POST"])
# def api_refine():
#     """Handles follow-up clarifications."""
#     data = request.get_json()
#     details = (data.get("details") or "").strip()
#     if not details:
#         return jsonify({"error": "Missing details"}), 400

#     if not session.get("conversation"):
#         return jsonify({"error": "No active conversation found."}), 400

#     last_query = session["conversation"][-1]["query"]
#     updated_query = f"{last_query}. Additional details: {details}"
#     print(f"🔁 Refining for user {session['user_id']} with extra details...")

#     refined_summary = run_pipeline(updated_query)

#     session["conversation"].append({
#         "query": updated_query,
#         "response": refined_summary
#     })
#     session.modified = True

#     return jsonify({
#         "query": updated_query,
#         "summary": refined_summary,
#         "conversation": session["conversation"]
#     })

# @app.route("/api/history", methods=["GET"])
# def api_history():
#     """Returns the full chat history for this session."""
#     return jsonify(session.get("conversation", []))

# @app.route("/api/reset", methods=["POST"])
# def api_reset():
#     """Resets the user's session (new conversation)."""
#     session["conversation"] = []
#     session.modified = True
#     return jsonify({"message": "Session reset successful."})

# # ============================================================
# # 6️⃣ Run Flask app
# # ============================================================

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)


# from flask import Flask, request, jsonify, render_template, session
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# import torch, os, uuid, pandas as pd
# from rapidfuzz import fuzz

# # ============================================================
# # 1️⃣ Flask setup and secret key
# # ============================================================

# app = Flask(__name__)
# app.secret_key = "supersecretkey_change_this"

# # ============================================================
# # 2️⃣ Load model once globally
# # ============================================================

# print("🚀 Loading LLaMA-3 model ...")
# MODEL_ID = "./7B-v0.3" if os.path.isdir("./7B-v0.3") else "meta-llama/Meta-Llama-3-8B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# try:
#     bnb_config = BitsAndBytesConfig(
#         load_in_4bit=True,
#         bnb_4bit_quant_type="nf4",
#         bnb_4bit_compute_dtype=torch.float16,
#     )
# except Exception:
#     bnb_config = None

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_ID,
#     device_map="auto",
#     quantization_config=bnb_config,
#     dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
# )
# model.eval()
# print(f"✅ Model loaded: {MODEL_ID}")

# # ============================================================
# # 3️⃣ Load Home Remedies CSV
# # ============================================================

# try:
#     remedies_df = pd.read_csv("Home Remedies.csv")
#     remedies_df.columns = [c.strip().lower() for c in remedies_df.columns]
#     print(f"✅ Loaded {len(remedies_df)} home remedies.")
# except Exception as e:
#     print(f"⚠️ Could not load remedies file: {e}")
#     remedies_df = pd.DataFrame()

# # ============================================================
# # 4️⃣ Session setup
# # ============================================================

# @app.before_request
# def ensure_session():
#     if "user_id" not in session:
#         session["user_id"] = str(uuid.uuid4())
#     if "conversation" not in session:
#         session["conversation"] = []

# # ============================================================
# # 5️⃣ Helpers
# # ============================================================

# @torch.inference_mode()
# def generate_response(prompt, max_tokens=800, temperature=0.7):
#     formatted = f"[INST] {prompt} [/INST]"
#     inputs = tokenizer(formatted, return_tensors="pt", padding=True,
#                        truncation=True, max_length=4096).to(model.device)
#     outputs = model.generate(**inputs, max_new_tokens=max_tokens,
#                              temperature=temperature, do_sample=True,
#                              pad_token_id=tokenizer.pad_token_id,
#                              eos_token_id=tokenizer.eos_token_id)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()

# DOMAINS = ["neurology", "general medicine", "ophthalmology", "dermatology", "psychology"]

# def run_pipeline(query):
#     """Detailed reasoning followed by summarization."""
#     # Step 1: domain detection
#     prompt1 = f"""Classify this query into 3–5 relevant medical domains:
# {', '.join(DOMAINS)}

# Query: "{query}".
# Return a comma-separated list."""
#     analysis = generate_response(prompt1, max_tokens=80)
#     relevant = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5] or DOMAINS[:3]

#     # Steps 2–6: detailed specialist reasoning
#     detailed_responses = []
#     for d in relevant:
#         prompt_detailed = f"""You are a {d} specialist doctor.
# Query: "{query}"

# Provide a DETAILED medical discussion in 4 sections:
# 1. Explanation of symptoms (2–3 paragraphs)
# 2. Possible causes (list and explain each)
# 3. Common treatments and management options
# 4. Safe home care tips and prevention advice"""
#         detailed_output = generate_response(prompt_detailed, max_tokens=400)
#         detailed_responses.append(f"--- {d.title()} ---\n{detailed_output}")

#     # Step 7: summarizer
#     combined = "\n\n".join(detailed_responses)
#     summary_prompt = f"""You are a professional medical summarizer.
# Summarize the following expert notes into 3 concise, patient-friendly paragraphs.
# Each paragraph should clearly explain:
# - Key symptoms and causes
# - Safe, practical home advice
# - When the patient should see a doctor

# Avoid repeating doctor names or the words 'query' or 'summarizer'.

# Expert Notes:
# {combined}
# """
#     summary = generate_response(summary_prompt, max_tokens=350)
#     return summary, detailed_responses

# # ============================================================
# # 6️⃣ Home remedy matcher (fuzzy)
# # ============================================================

# def find_remedies(summary_text):
#     results = []
#     if remedies_df.empty:
#         return results
#     text_lower = summary_text.lower()
#     for _, row in remedies_df.iterrows():
#         condition = str(row.get("condition", "")).lower()
#         if condition:
#             score = fuzz.partial_ratio(condition, text_lower)
#             if score > 70:
#                 results.append({
#                     "condition": row.get("condition", ""),
#                     "remedy": row.get("remedy", ""),
#                     "yoga": row.get("yoga", ""),
#                     "image": row.get("image_url", "")
#                 })
#     return results

# # ============================================================
# # 7️⃣ Routes
# # ============================================================

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/api/query", methods=["POST"])
# def api_query():
#     data = request.get_json()
#     query = (data.get("query") or "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     print(f"🩺 Query from {session['user_id']}: {query}")
#     summary, details = run_pipeline(query)
#     remedies = find_remedies(summary)

#     session["conversation"].append({"query": query, "summary": summary, "details": details})
#     session.modified = True

#     return jsonify({
#         "query": query,
#         "summary": summary,
#         "details": details,
#         "remedies": remedies
#     })

# @app.route("/api/refine", methods=["POST"])
# def api_refine():
#     data = request.get_json()
#     details = (data.get("details") or "").strip()
#     if not details:
#         return jsonify({"error": "Missing details"}), 400

#     last_query = session["conversation"][-1]["query"]
#     updated_query = f"{last_query}. Additional details: {details}"
#     print(f"🔁 Refining query: {updated_query}")

#     summary, detailed_responses = run_pipeline(updated_query)
#     remedies = find_remedies(summary)

#     session["conversation"].append({"query": updated_query, "summary": summary, "details": detailed_responses})
#     session.modified = True

#     return jsonify({
#         "query": updated_query,
#         "summary": summary,
#         "details": detailed_responses,
#         "remedies": remedies
#     })

# @app.route("/api/learn_more", methods=["POST"])
# def api_learn_more():
#     """Generate a short safety guide for a remedy or yoga."""
#     data = request.get_json()
#     topic = (data.get("topic") or "").strip()
#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     prompt = f"""Provide a 3-4 sentence safe usage and benefit guide for: {topic}.
# Include how it helps, precautions, and when to avoid it."""
#     guide = generate_response(prompt, max_tokens=150)
#     return jsonify({"topic": topic, "guide": guide})

# @app.route("/api/reset", methods=["POST"])
# def api_reset():
#     session["conversation"] = []
#     session.modified = True
#     return jsonify({"message": "Session reset successful."})

# # ============================================================
# # 8️⃣ Run app
# # ============================================================

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)

from flask import Flask, request, jsonify, render_template, session
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch, os, uuid, pandas as pd
from rapidfuzz import fuzz

# ============================================================
# 1️⃣ Flask setup
# ============================================================

app = Flask(__name__)
app.secret_key = "supersecretkey_change_this"  # change in production

# ============================================================
# 2️⃣ Load model once globally
# ============================================================

print("🚀 Loading LLaMA-3 model ...")
MODEL_ID = "./7B-v0.3" if os.path.isdir("./7B-v0.3") else "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

try:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
except Exception:
    bnb_config = None

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    quantization_config=bnb_config,
    dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
)
model.eval()
print(f"✅ Model loaded: {MODEL_ID}")

# ============================================================
# 3️⃣ Load Home Remedies CSV
# ============================================================

try:
    remedies_df = pd.read_csv("Home Remedies.csv")
    remedies_df.columns = [c.strip().lower() for c in remedies_df.columns]
    print(f"✅ Loaded {len(remedies_df)} home remedies.")
except Exception as e:
    print(f"⚠️ Could not load remedies file: {e}")
    remedies_df = pd.DataFrame()

# ============================================================
# 4️⃣ Ensure session
# ============================================================

@app.before_request
def ensure_session():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    if "conversation" not in session:
        session["conversation"] = []

# ============================================================
# 5️⃣ Helper: multi-pass generation to prevent cutoff
# ============================================================

@torch.inference_mode()
def generate_response(prompt, max_tokens=1200, temperature=0.7):
    """
    Generates complete long-form responses; continues generation
    automatically if text is truncated mid-sentence.
    """
    formatted = f"[INST] {prompt} [/INST]"
    inputs = tokenizer(formatted, return_tensors="pt", padding=True,
                       truncation=True, max_length=8192).to(model.device)

    full_output = ""
    current_input = inputs
    for i in range(3):
        outputs = model.generate(
            **current_input,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        piece = decoded.split("[/INST]")[-1].strip()
        full_output += piece
        if full_output.endswith((".", "!", "?")) or len(piece) < (max_tokens * 0.9):
            break
        current_input = tokenizer(full_output, return_tensors="pt").to(model.device)
    return full_output.strip()

# ============================================================
# 6️⃣ Improved pipeline for structured, user-friendly answers
# ============================================================

DOMAINS = ["neurology", "general medicine", "ophthalmology", "dermatology", "psychology"]

def run_pipeline(query):
    """Runs full structured pipeline with formatted output."""
    # Step 1: domain classification
    prompt1 = f"""You are a medical domain classifier.
Classify the following user query into 3–5 most relevant domains from:
{', '.join(DOMAINS)}.

Query: "{query}"
Return a comma-separated list."""
    analysis = generate_response(prompt1, max_tokens=80)
    relevant = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5] or DOMAINS[:3]

    # Step 2–6: detailed reasoning per specialist
    specialists = []
    for d in relevant:
        p = f"""You are a {d} specialist doctor.
Query: "{query}"

Provide your analysis using this structure:
1️⃣ **Symptoms & Causes** – summarize the main symptoms and list 3–5 likely causes.
2️⃣ **Home Remedies & Care** – list safe, practical things a patient can do at home.
3️⃣ **Doctor’s Recommendations** – give evidence-based medical guidance and warning signs.
4️⃣ **Yoga / Lifestyle Advice** – mention any helpful yoga poses or habits.

Be empathetic, concise, and medically responsible.
"""
        specialists.append(f"--- {d.title()} ---\n{generate_response(p, max_tokens=700)}")

    # Step 7: final structured summarization
    combined = "\n\n".join(specialists)
    summary_prompt = f"""You are a professional medical summarizer.
Below are expert notes from multiple specialists for the query: "{query}".

Write a single, clean, patient-friendly final answer using this format:

### 🧠 Key Symptoms & Causes
• ...
• ...

### 🏠 Home Remedies & Lifestyle Tips
• ...
• ...

### 👩‍⚕️ Doctor’s Recommendations
• ...
• ...

### 🩺 Summary
(2–3 concise, compassionate sentences summarizing advice)

Tone: warm, clear, factual, and medically safe.
Do NOT repeat system text or specialist names.

Expert Notes:
{combined}
"""
    summary = generate_response(summary_prompt, max_tokens=700)
    return summary, specialists

# ============================================================
# 7️⃣ Remedy matching (fuzzy)
# ============================================================

def find_remedies(summary_text):
    """Match conditions in text with home remedies."""
    results = []
    if remedies_df.empty:
        return results
    text_lower = summary_text.lower()
    for _, row in remedies_df.iterrows():
        condition = str(row.get("condition", "")).lower()
        if condition:
            score = fuzz.partial_ratio(condition, text_lower)
            if score > 70:
                results.append({
                    "condition": row.get("condition", ""),
                    "remedy": row.get("remedy", ""),
                    "yoga": row.get("yoga", ""),
                    "image": row.get("image_url", "")
                })
    return results

# ============================================================
# 8️⃣ Flask routes
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json()
    query = (data.get("query") or "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400
    print(f"🩺 Query from {session['user_id']}: {query}")
    summary, details = run_pipeline(query)
    remedies = find_remedies(summary)
    session["conversation"].append({"query": query, "summary": summary, "details": details})
    session.modified = True
    return jsonify({
        "query": query,
        "summary": summary,
        "details": details,
        "remedies": remedies
    })

@app.route("/api/refine", methods=["POST"])
def api_refine():
    data = request.get_json()
    details = (data.get("details") or "").strip()
    if not details:
        return jsonify({"error": "Missing details"}), 400
    last_query = session["conversation"][-1]["query"]
    updated_query = f"{last_query}. Additional details: {details}"
    print(f"🔁 Refining: {updated_query}")
    summary, detailed = run_pipeline(updated_query)
    remedies = find_remedies(summary)
    session["conversation"].append({"query": updated_query, "summary": summary, "details": detailed})
    session.modified = True
    return jsonify({
        "query": updated_query,
        "summary": summary,
        "details": detailed,
        "remedies": remedies
    })

@app.route("/api/learn_more", methods=["POST"])
def api_learn_more():
    data = request.get_json()
    topic = (data.get("topic") or "").strip()
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    prompt = f"""Provide a 3–4 sentence safe usage and benefits guide for {topic}.
Explain how it helps, precautions, and when to avoid it."""
    guide = generate_response(prompt, max_tokens=200)
    return jsonify({"topic": topic, "guide": guide})

@app.route("/api/reset", methods=["POST"])
def api_reset():
    session["conversation"] = []
    session.modified = True
    return jsonify({"message": "Session reset successful."})

# ============================================================
# 9️⃣ Run app
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

