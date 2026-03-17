# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     BitsAndBytesConfig,
# )
# import torch
# import os

# # ============================================================
# # 1) Load Meta-Llama-3-8B-Instruct from Hugging Face
# # ============================================================

# def load_model(model_id="meta-llama/Meta-Llama-3-8B-Instruct"):
#     """
#     Loads LLaMA-3-8B-Instruct with 4-bit quantization for VRAM efficiency.
#     Requires GPU with ≥ 12 GB VRAM and Hugging Face token.
#     """
#     try:
#         # Check for Hugging Face token
#         if not os.getenv("HF_TOKEN"):
#             print("⚠️ Hugging Face token not found. Set HF_TOKEN environment variable or run 'huggingface_hub login'.")
#             return None, None

#         print(f"🚀 Loading model: {model_id}")

#         # Load tokenizer
#         tokenizer = AutoTokenizer.from_pretrained(model_id)
#         if tokenizer.pad_token is None:
#             tokenizer.pad_token = tokenizer.eos_token
#             tokenizer.pad_token_id = tokenizer.eos_token_id
#         print("✅ Tokenizer loaded successfully.")

#         # Configure 4-bit quantization (if available)
#         bnb_config = None
#         if torch.cuda.is_available():
#             try:
#                 bnb_config = BitsAndBytesConfig(
#                     load_in_4bit=True,
#                     bnb_4bit_quant_type="nf4",
#                     bnb_4bit_compute_dtype=torch.float16,
#                 )
#                 print("✅ 4-bit quantization configured.")
#             except Exception as e:
#                 print(f"⚠️ 4-bit quantization unavailable: {e}")
#         else:
#             print("⚠️ No GPU detected, falling back to CPU with float32.")

#         # Load model
#         model = AutoModelForCausalLM.from_pretrained(
#             model_id,
#             device_map="auto",
#             quantization_config=bnb_config,
#             torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
#             low_cpu_mem_usage=True,
#         )
#         print("✅ LLaMA-3 model loaded successfully.")
#         return tokenizer, model
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         return None, None

# # ============================================================
# # 2) Generation Helper
# # ============================================================

# def generate_response(tokenizer, model, prompt, max_new_tokens=500, temperature=0.7):
#     """
#     Generates a response using LLaMA-3 with instruction formatting.
#     max_new_tokens set to 500 for concise, efficient responses.
#     """
#     try:
#         print("📝 Generating response...")
#         formatted_prompt = f"[INST] {prompt} [/INST]"
#         inputs = tokenizer(
#             formatted_prompt,
#             return_tensors="pt",
#             padding=True,
#             truncation=True,
#             max_length=2048,  # Reduced for efficiency
#         ).to(model.device)
#         print(f"✅ Input tokenized, length: {len(inputs['input_ids'][0])} tokens")

#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=max_new_tokens,
#             temperature=temperature,
#             do_sample=True if temperature > 0 else False,
#             pad_token_id=tokenizer.pad_token_id,
#             eos_token_id=tokenizer.eos_token_id,
#             top_p=0.9 if temperature > 0 else 1.0,
#         )
#         print("✅ Generation complete.")

#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         generated_text = response.split("[/INST]")[-1].strip()
#         if not generated_text:
#             print("⚠️ No text generated after decoding.")
#             return "Error: No response generated."
#         print(f"✅ Response decoded: {generated_text[:50]}...")
#         return generated_text
#     except Exception as e:
#         print(f"⚠️ Generation error: {e}")
#         return f"Error: Failed to generate response: {e}"

# # ============================================================
# # 3) Medical Reasoning Pipeline
# # ============================================================

# DOMAINS = [
#     "cardiology",
#     "neurology",
#     "pulmonology",
#     "gastroenterology",
#     "endocrinology",
#     "dermatology",
#     "ophthalmology",
#     "nephrology",
#     "urology",
#     "psychiatry",
#     "rheumatology",
#     "hematology",
#     "oncology",
#     "pediatrics",
#     "gynecology",
#     "orthopedics",
#     "ENT",
#     "infectious_diseases",
#     "general_medicine",
#     "internal_medicine",
# ]

# def run_pipeline(query):
#     """
#     Processes a medical query through domain classification, specialist insights, and synthesis.
#     """
#     print(f"🚀 Starting pipeline for query: {query}")
#     tokenizer, model = load_model()
#     if not model or not tokenizer:
#         return "Error: Model or tokenizer failed to load."

#     responses = {}

#     # Step 1: Domain Classification
#     print("🔍 Classifying domains...")
#     prompt1 = f"""You are a medical query analyzer. 
# Analyze the user's query and identify relevant medical domains.
# Query: "{query}"
# Task: Select 3–5 relevant domains from: {', '.join(DOMAINS)}.
# Return only a comma-separated list (e.g., 'neurology, psychology')."""
#     analysis = generate_response(tokenizer, model, prompt1, max_new_tokens=100, temperature=0.1)
#     print(f"✅ Domain classification result: {analysis}")
#     relevant_domains = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5]
#     if not relevant_domains:
#         print("⚠️ No valid domains identified, defaulting to first three domains.")
#         relevant_domains = DOMAINS[:3]
#     responses["analysis"] = analysis

#     # Step 2–6: Specialist Responses
#     print(f"🩺 Generating specialist responses for domains: {relevant_domains}")
#     for domain in relevant_domains:
#         prompt_specialist = f"""You are a {domain} specialist doctor.
# Query: "{query}"
# Provide concise, safe, evidence-based information.
# Format:
# Insights: [2–3 bullet points]
# Causes: [2–3 bullet points]
# Recommendations: [2–3 bullet points]"""
#         response = generate_response(
#             tokenizer, model, prompt_specialist, max_new_tokens=500, temperature=0.3
#         )
#         responses[f"specialist_{domain}"] = response
#         print(f"✅ Generated response for {domain.title()}: {response[:50]}...")

#     # Step 7: Final Synthesis
#     print("📋 Synthesizing specialist responses...")
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
#     final_summary = generate_response(tokenizer, model, prompt7, max_new_tokens=1000, temperature=0.2)
#     print("✅ Final synthesis complete.")
#     return final_summary

# # ============================================================
# # 4) CLI Entry Point with Interaction
# # ============================================================

# if __name__ == "__main__":
#     query = input("Enter your medical query (e.g., 'persistent headaches'): ").strip()
#     if not query:
#         print("⚠️ Please enter a valid query.")
#     else:
#         print("\n=== 🩺 Final Summary ===\n")
#         response = run_pipeline(query)
#         if response.startswith("Error"):
#             print(f"❌ Pipeline failed: {response}")
#         else:
#             print(response)

#         # Interaction loop
#         while True:
#             satisfaction = input("\nAre you satisfied with the response? (yes/no): ").strip().lower()
#             if satisfaction == "yes":
#                 print("Thank you for using the medical query system!")
#                 break
#             elif satisfaction == "no":
#                 second_query = input("Please enter a follow-up query to clarify or add details: ").strip()
#                 if not second_query:
#                     print("⚠️ Please enter a valid follow-up query.")
#                     continue
#                 # Concatenate the original and follow-up query
#                 combined_query = f"{query}. Additional details: {second_query}"
#                 print("\n=== 🩺 Updated Final Summary ===\n")
#                 response = run_pipeline(combined_query)
#                 if response.startswith("Error"):
#                     print(f"❌ Pipeline failed: {response}")
#                 else:
#                     print(response)
#                 # Ask again after processing the combined query
#                 continue
#             else:
#                 print("⚠️ Please enter 'yes' or 'no'.")
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# ============================================================
# 1) Load model
# ============================================================

def load_model(model_id="meta-llama/Meta-Llama-3-8B-Instruct"):
    """Load the LLaMA-3 model (optionally quantized)."""
    print(f"🚀 Loading model: {model_id}")

    tokenizer = AutoTokenizer.from_pretrained(model_id)
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
        model_id,
        device_map="auto",
        quantization_config=bnb_config,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    print("✅ Model loaded successfully.\n")
    return tokenizer, model


# ============================================================
# 2) Generate clean short summary
# ============================================================

def generate_summary(tokenizer, model, query):
    """Generate a short, clean medical summary (2–3 lines)."""
    prompt = (
        f"You are a helpful medical assistant.\n"
        f"User question: {query}\n"
        f"Give a brief, clear summary (2–3 lines, plain text)."
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048,
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        temperature=0.6,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove leftover tokens, system text, or prompt echoes
    response = response.replace(prompt, "").strip()
    response = response.replace("[INST]", "").replace("[/INST]", "").strip()

    # Fallback: if blank, retry with simpler generation
    if not response:
        response = "I'm sorry, I couldn't generate a summary. Please try rephrasing your question."

    return response


# ============================================================
# 3) Terminal app
# ============================================================

def main():
    tokenizer, model = load_model()
    query = input("\n🩺 Enter your medical question: ").strip()
    if not query:
        print("⚠️ Please enter a valid query.")
        return

    print("\n💬 Generating summary...\n")
    summary = generate_summary(tokenizer, model, query)
    print("🧠 Summary:\n", summary)
    print("\n✅ Done.\n")


# ============================================================
# 4) Run
# ============================================================

if __name__ == "__main__":
    main()
