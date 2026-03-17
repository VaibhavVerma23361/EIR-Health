# ============================================================
# pipeline_runner.py
# ============================================================

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch, os

# Load model once globally (not on each call)
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
# 1) Base generation function
# ============================================================

@torch.inference_mode()
def generate_response(prompt: str, max_tokens=300, temperature=0.7):
    """Generate text from LLaMA model."""
    formatted_prompt = f"[INST] {prompt} [/INST]"
    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=4096,
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text.split("[/INST]")[-1].strip()

# ============================================================
# 2) Multi-specialist medical reasoning pipeline
# ============================================================

DOMAINS = [
    "neurology",
    "general medicine",
    "ophthalmology",
    "dermatology",
    "psychology",
]

def run_pipeline(query: str):
    """Run full medical reasoning pipeline on a query."""
    responses = {}

    # Step 1: Domain classification
    prompt1 = f"""You are a medical query analyzer. 
Analyze the user's query and identify relevant medical domains.
Query: "{query}"
Task: Select 3–5 relevant domains from: {', '.join(DOMAINS)}.
Return only a comma-separated list (e.g., 'neurology, psychology')."""
    analysis = generate_response(prompt1, max_tokens=60)
    relevant_domains = [d.strip() for d in analysis.split(",") if d.strip() in DOMAINS][:5]
    if not relevant_domains:
        relevant_domains = DOMAINS[:3]
    responses["analysis"] = analysis

    # Step 2–6: Specialist insights
    for domain in relevant_domains:
        prompt_specialist = f"""You are a {domain} specialist doctor.
Query: "{query}"
Provide concise, safe, evidence-based insights.
Format strictly:
Insights: [2–3 bullet points]
Causes: [2–3 bullet points]
Recommendations: [2–3 bullet points]"""
        specialist_response = generate_response(prompt_specialist, max_tokens=150)
        responses[f"specialist_{domain}"] = specialist_response

    # Step 7: Summarize all specialists
    specialists_summary = "\n\n".join(
        f"{d.replace('specialist_', '').title()}:\n{r}"
        for d, r in responses.items()
        if "specialist_" in d
    )

    prompt7 = f"""You are a medical summarizer. Combine the following specialist outputs into one coherent summary.
{specialists_summary}

Output format:
Key Symptoms/Causes: [short summarized list]
Recommendations: [safe, consensus-based advice]
When to See a Doctor: [clear warning conditions]"""

    final_summary = generate_response(prompt7, max_tokens=300)
    responses["final_summary"] = final_summary

    return responses
