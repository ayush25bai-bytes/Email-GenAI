import os
import re
import json
import math
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, set_key

# --- 1. SETUP & ENVIRONMENT (Original Checks Retained) ---
current_dir = Path(__file__).parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

def get_api_key():
    """Checks for API key, prompts user and saves to .env if missing."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n🔑 GROQ_API_KEY not found in environment.")
        api_key = input("Please enter your Groq API Key: ").strip()
        if not api_key:
            print("❌ Error: API Key is required to run this script.")
            exit(1)
        
        # Save to .env file for future use
        set_key(str(env_path), "GROQ_API_KEY", api_key)
        print(f"✅ API Key saved locally to: {env_path}")
    
    return api_key

GROQ_API_KEY = get_api_key()

try:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
except ImportError:
    print("❌ ERROR: Missing dependencies. Run: pip install groq python-dotenv")
    exit(1)

# --- 2. UTILITY FUNCTIONS ---
def slugify(text: str) -> str:
    """Converts subjects into filesystem-friendly filenames."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:80]

# --- 3. THE EMAIL ENGINE ---
def generate_structured_email():
    print("\n" + "═"*60)
    print("📧 EMAIL ARCHITECT - PROFESSIONAL DRAFTING")
    print("═"*60)

    # User Inputs based on the visual template provided
    sender_name = input("👤 Your Full Name: ").strip()
    sender_email = input("📧 Your Email Address: ").strip()
    recipient_name = input("👤 Recipient Name: ").strip()
    recipient_email = input("📧 Recipient Email: ").strip()
    
    cc = input("👥 CC (optional, comma separated): ").strip()
    bcc = input("🔒 BCC (optional, comma separated): ").strip()
    
    topic_goal = input("🎯 Purpose of Email (e.g., Requesting the Marks Report): ").strip()
    tone = input("🎭 Tone (Professional, Urgent, Casual) [Default: Professional]: ").strip() or "Professional"

    if not topic_goal or not recipient_name:
        print("❌ Error: Purpose and Recipient are required.")
        return

    print(f"\n🚀 Drafting content following visual hierarchy...")

    # -- STEP 1: GENERATE SUBJECT & METADATA --
    meta_prompt = f"""
    Generate professional email metadata for:
    - Goal: {topic_goal}
    - Recipient: {recipient_name}
    - Tone: {tone}

    Return ONLY a valid JSON object:
    {{
      "subject": "Clear & professional subject line",
      "salutation": "Appropriate opening (e.g., Dear {recipient_name}:)",
      "closing": "Professional sign-off (e.g., Regards, or Sincerely,)"
    }}
    """
    
    try:
        meta_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": meta_prompt}],
            temperature=0.7
        )
        raw_json = meta_res.choices[0].message.content.strip().replace("```json", "").replace("```", "")
        meta_data = json.loads(raw_json)
    except Exception as e:
        meta_data = {
            "subject": f"Update regarding: {topic_goal}",
            "salutation": f"Dear {recipient_name}:",
            "closing": "Regards,"
        }

    # -- STEP 2: GENERATE MESSAGE CONTENT --
    content_prompt = f"""
    You are an expert communicator. Write the body of an email based on these details:
    
    GOAL: {topic_goal}
    RECIPIENT: {recipient_name}
    TONE: {tone}
    
    STRICT RULES:
    1. Directness: Start with the main request or update immediately.
    2. Length: Maximum 2 concise paragraphs.
    3. Formatting: Use plain text. No "AI-isms" like "I hope this finds you well."
    4. Provide ONLY the message body content.
    """

    content_res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": content_prompt}],
        temperature=0.5
    )
    message_body = content_res.choices[0].message.content.strip()

    # -- STEP 3: ASSEMBLE ACCORDING TO TEMPLATE --
    # Constructing the final string to match the requested image layout
    final_email = [
        f"FROM:    {sender_name} <{sender_email}>",
        f"TO:      {recipient_name} <{recipient_email}>"
    ]
    
    if cc: final_email.append(f"CC:      {cc}")
    if bcc: final_email.append(f"BCC:     {bcc}")
    
    final_email.append(f"SUBJECT: {meta_data['subject']}")
    final_email.append("\n" + "─"*40 + "\n") # Visual separator
    final_email.append(meta_data['salutation'])
    final_email.append(f"\n{message_body}\n")
    final_email.append(meta_data['closing'])
    final_email.append(sender_name.split()[0]) # Just first name for the closing signature
    
    # Signature File Block
    final_email.append("\n--")
    final_email.append(sender_name)
    final_email.append(f"Email: {sender_email}")
    final_email.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    full_text = "\n".join(final_email)

    # --- 4. SAVING LOGIC ---
    drafts_folder = current_dir / "email_drafts"
    drafts_folder.mkdir(exist_ok=True)
    
    file_path = drafts_folder / f"{slugify(meta_data['subject'])}.txt"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"\n" + "═"*60)
    print(f"✅ SUCCESS: Formatted Email Drafted!")
    print(f"📂 Saved to: {file_path.absolute()}")
    print("═"*60 + "\n")

if __name__ == "__main__":
    generate_structured_email()