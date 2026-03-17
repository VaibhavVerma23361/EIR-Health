# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     BitsAndBytesConfig,
# )
# import torch


# # ============================================================
# # 1) Load Meta-Llama-3-8B-Instruct from Hugging Face
# # ============================================================

# def load_model(model_id="meta-llama/Meta-Llama-3-8B-Instruct"):
#     """
#     Loads LLaMA-3-8B-Instruct with automatic 4-bit quantization if bitsandbytes is installed.
#     Works out-of-the-box on GPUs ≥ 12 GB.
#     """
#     try:
#         print(f"🚀 Loading model: {model_id}")

#         # Load tokenizer
#         tokenizer = AutoTokenizer.from_pretrained(model_id)
#         if tokenizer.pad_token is None:
#             tokenizer.pad_token = tokenizer.eos_token

#         # Optional 4-bit quantization (saves VRAM)
#         try:
#             bnb_config = BitsAndBytesConfig(
#                 load_in_4bit=True,
#                 bnb_4bit_quant_type="nf4",
#                 bnb_4bit_compute_dtype=torch.float16,
#             )
#         except Exception:
#             bnb_config = None

#         # Load model
#         model = AutoModelForCausalLM.from_pretrained(
#             model_id,
#             device_map="auto",
#             quantization_config=bnb_config,
#             torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
#         )

#         print("✅ LLaMA-3 model and tokenizer loaded successfully.")
#         return tokenizer, model
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         return None, None


# # ============================================================
# # 2) Generation helper
# # ============================================================

# def generate_response(tokenizer, model, prompt, max_tokens=1000, temperature=0.7):
#     """
#     Generates a response from the model using the LLaMA-3 instruction format.
#     """
#     try:
#         formatted_prompt = f"[INST] {prompt} [/INST]"
#         inputs = tokenizer(formatted_prompt, return_tensors="pt", padding=True, truncation=True, max_length=8000).to(model.device)

#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=max_tokens,
#             temperature=temperature,
#             do_sample=True,
#             pad_token_id=tokenizer.pad_token_id,
#             eos_token_id=tokenizer.eos_token_id,
#         )

#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         # Strip the prompt portion
#         return response.split("[/INST]")[-1].strip()
#     except Exception as e:
#         return f"⚠️ Generation error: {e}"


# # ============================================================
# # 3) Medical reasoning pipeline
# # ============================================================

# DOMAINS = [
#     "neurology",
#     "general medicine",
#     "ophthalmology",
#     "dermatology",
#     "psychology",
# ]


# def run_pipeline(query):
#     tokenizer, model = load_model()
#     if not model or not tokenizer:
#         return "Error: Model or tokenizer failed to load."

#     responses = {}

#     # Step 1: Domain classification
#     prompt1 = f"""You are a medical query analyzer. 
# Analyze the user's query and identify relevant medical domains.
# Query: "{query}"
# Task: Select 3–5 relevant domains from: {', '.join(DOMAINS)}.
# Return only a comma-separated list (e.g., 'neurology, psychology')."""
#     analysis = generate_response(tokenizer, model, prompt1, max_tokens=1000)
#     relevant_domains = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5]
#     if not relevant_domains:
#         relevant_domains = DOMAINS[:3]
#     responses["analysis"] = analysis

#     # Step 2–6: Specialist responses
#     for domain in relevant_domains:
#         prompt_specialist = f"""You are a {domain} specialist doctor.
# Query: "{query}"
# Provide concise, safe, evidence-based information.
# Format:
# Insights: [2–3 bullet points]
# Causes: [2–3 bullet points]
# Recommendations: [2–3 bullet points]"""
#         responses[f"specialist_{domain}"] = generate_response(
#             tokenizer, model, prompt_specialist, max_tokens=1000
#         )

#     # Step 7: Final synthesis
#     specialists_summary = "\n\n".join(
#         f"{d.replace('specialist_', '').title()}:\n{r}"
#         for d, r in responses.items()
#         if "specialist_" in d
#     )

#     prompt7 = f"""You are a medical summarizer. Combine the following specialist outputs into a coherent summary.
# {specialists_summary}

# Output format:
# Key Symptoms/Causes: [summarized list]
# Recommendations: [safe, consensus-based advice]
# When to See a Doctor: [clear warning conditions]"""
#     final_summary = generate_response(tokenizer, model, prompt7, max_tokens=500)
#     return final_summary


# # ============================================================
# # 4) CLI entry point
# # ============================================================

# if __name__ == "__main__":
#     query = input("Enter your medical query (e.g., 'persistent headaches'): ").strip()
#     if query:
#         print("\n=== 🩺 Final Summary ===\n")
#         print(run_pipeline(query))
#     else:
#         print("⚠️ Please enter a valid query.")




from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)
import torch

# ============================================================
# 1) Load Meta-Llama-3-8B-Instruct (only once)
# ============================================================

def load_model(model_id="meta-llama/Meta-Llama-3-8B-Instruct"):
    """Loads LLaMA-3-8B-Instruct with optional 4-bit quantization."""
    try:
        print(f"🚀 Loading model: {model_id}")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Optional 4-bit quantization (saves VRAM)
        try:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
        except Exception:
            bnb_config = None

        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            quantization_config=bnb_config,
            dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        )

        print("✅ LLaMA-3 model and tokenizer loaded successfully.\n")
        return tokenizer, model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None


# ============================================================
# 2) Generation helper
# ============================================================

def generate_response(tokenizer, model, prompt, max_tokens=1000, temperature=0.7):
    """Generates a response using LLaMA-3 instruction format."""
    try:
        formatted_prompt = f"[INST] {prompt} [/INST]"
        inputs = tokenizer(
            formatted_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=8000,
        ).to(model.device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("[/INST]")[-1].strip()
    except Exception as e:
        return f"⚠️ Generation error: {e}"


# ============================================================
# 3) Multi-specialist pipeline
# ============================================================

DOMAINS = [
    "cardiology",
    "neurology",
    "pulmonology",
    "gastroenterology",
    "endocrinology",
    "dermatology",
    "ophthalmology",
    "nephrology",
    "urology",
    "psychiatry",
    "rheumatology",
    "hematology",
    "oncology",
    "pediatrics",
    "gynecology",
    "orthopedics",
    "ENT",
    "infectious_diseases",
    "general_medicine",
    "internal_medicine",
]

def run_pipeline(query, tokenizer, model):
    """Runs the full reasoning pipeline and returns the summarizer output."""
    responses = {}

    # Step 1: Domain classification
    prompt1 = f"""You are a medical query analyzer.
Analyze the user's query and identify relevant medical domains.
Query: "{query}"
Task: Select 3–5 relevant domains from: {', '.join(DOMAINS)}.
Return only a comma-separated list (e.g., 'neurology, psychology')."""
    analysis = generate_response(tokenizer, model, prompt1, max_tokens=100)
    relevant_domains = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5]
    if not relevant_domains:
        relevant_domains = DOMAINS[:3]
    responses["analysis"] = analysis

    # Step 2–6: Specialist responses
    for domain in relevant_domains:
        prompt_specialist = f"""You are a {domain} specialist doctor.
Query: "{query}"
Provide concise, safe, evidence-based information.
Format:
Insights: [2–3 bullet points]
Causes: [2–3 bullet points]
Recommendations: [2–3 bullet points]"""
        responses[f"specialist_{domain}"] = generate_response(
            tokenizer, model, prompt_specialist, max_tokens=300
        )

    # Step 7: Final summarizer
    specialists_summary = "\n\n".join(
        f"{d.replace('specialist_', '').title()}:\n{r}"
        for d, r in responses.items()
        if "specialist_" in d
    )

    prompt7 = f"""You are a medical summarizer. Combine the following specialist outputs into a coherent summary.
{specialists_summary}

Output format:
Key Symptoms/Causes: [summarized list]
Recommendations: [safe, consensus-based advice]
When to See a Doctor: [clear warning conditions]"""

    final_summary = generate_response(tokenizer, model, prompt7, max_tokens=2048)
    return final_summary


# ============================================================
# 4) Interactive refinement loop
# ============================================================

def interactive_medical_assistant():
    """Runs the conversational refinement loop."""
    query = input("Enter your medical query (e.g., 'persistent headaches'): ").strip()
    if not query:
        print("⚠️ Please enter a valid query.")
        return

    # Load model once
    tokenizer, model = load_model()
    if not model or not tokenizer:
        print("❌ Model failed to load.")
        return

    # First pass
    print("\n=== 🩺 Initial Medical Summary ===\n")
    summary = run_pipeline(query, tokenizer, model)
    print(summary)
    print("\n")

    # Feedback loop
    while True:
        feedback = input("Are you satisfied with the answer? (Yes/No): ").strip().lower()
        if feedback in ("yes", "y"):
            print("\n✅ Thank you. Stay healthy!")
            break
        elif feedback in ("no", "n"):
            followup = input("\nPlease describe your symptoms or concerns in more detail:\n> ").strip()
            if not followup:
                print("⚠️ No clarification provided. Ending session.")
                break
            # Combine old and new info for better reasoning
            updated_query = f"{query}. Additional details: {followup}"
            print("\n=== 🔁 Refining diagnosis based on new details... ===\n")
            new_summary = run_pipeline(updated_query, tokenizer, model)
            print(new_summary)
            print("\n")
            query = updated_query  # update context for next loop
        else:
            print("⚠️ Please answer Yes or No.\n")


# ============================================================
# 5) CLI entry point
# ============================================================

if __name__ == "__main__":
    interactive_medical_assistant()
