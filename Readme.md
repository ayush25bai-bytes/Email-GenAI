# 📧 Professional Email Architect

A high-performance Python CLI tool that transforms a simple goal into a perfectly structured, high-impact professional email. Designed for executives, entrepreneurs, and busy professionals who need **clear communication** with a **standardized corporate layout**.

## ✨ Features

* **Visual Correspondence:** Generates drafts that follow a strict professional email UI (From, To, CC, BCC, Subject, and Signature File).
* **Dual-Stage Precision:** * **Stage 1:** Generates a high-open-rate Subject Line and Preview Text.
    * **Stage 2:** Drafts a concise, "no-fluff" body using an Elite Executive Assistant persona.
* **Anti-AI Guardrails:** Explicitly avoids generic clichés like *"I hope this email finds you well,"* ensuring the tone feels authentic and human.
* **Automatic Formatting:** * `--` Signature blocks for professional contact info.
    * `─` Visual separators for easy reading in text editors.
* **Smart File Management:** Saves drafts as `.txt` files in an `/email_drafts` folder using "slugified" subject lines for easy retrieval.
* **Secure Persistence:** Manages your **Groq API Key** via a local `.env` file.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed and a **Groq API Key**. You can obtain one at [console.groq.com](https://console.groq.com/).

### 2. Installation
Install the necessary dependencies via pip:

```bash
pip install groq python-dotenv
```

### 3. Running the Architect
Launch the script from your terminal:

```bash
python email_generator.py
```

*Note: On your first run, the script will prompt you for your API Key and save it locally for future use.*

---

## 🛠️ How it Works

The script follows a rigorous professional communication workflow:

1.  **Context Input:** You provide the recipient, the specific goal (e.g., "Requesting the Q3 Report"), and the desired tone.
2.  **Metadata Generation:** The AI creates a context-aware Subject Line, Salutation, and Closing.
3.  **Drafting:** The engine writes a maximum of two concise paragraphs, focusing on a clear **Call to Action (CTA)**.
4.  **Assembly:** The script assembles the pieces into a standardized template that mirrors a modern email client's interface.

---

## 📂 Project Structure

```text
.
├── email_generator.py   # The main engine
├── .env                 # Your API keys (Private)
└── email_drafts/        # Output directory for your drafts
    └── request-for-meeting.txt
```

---

## 📖 Example Output Structure

The generated files are optimized for a quick "Copy-Paste" into Gmail, Outlook, or Apple Mail:

```text
FROM:    Samuel Allison <samuel.allison@xyz.com>
TO:      Karen Jones <karen.jones@lmno.com>
SUBJECT: Regarding: Marks Report Update

────────────────────────────────────────

Dear Karen:

Have you completed the revision of the Marks report? I would like to include a copy in my meeting with Rachel tomorrow.

I will be in my office until noon if you have any questions.

Regards,
Sam

--
Samuel Allison
Director, Marketing
XYZ, Inc.
```

---

## ⚖️ License
This project is open-source. Use it to communicate better!
