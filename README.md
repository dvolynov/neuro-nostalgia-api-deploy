# **Neuro-Nostalgia API**

This project provides a FastAPI-based solution for generating dynamic webpages, schemas, and CSS using multiple API versions, including integrations with Gemini and GPT-4o models. Each API version adds improvements such as schema generation, retro webpage generation, and CSS styling.

---

## **Project Structure**

```plaintext
Neuro-Nostalgia/
│— .venv/                        # Python virtual environment
│— api/
│   ├— tools/                    # Shared utilities (e.g., bots)
│   │   ├— __init__.py
│   │   └— bot.py
│   ├— v1/                       # API Version 1
│   │   ├— instructions/         # Input schema/text instructions
│   │   │   ├— html.txt
│   │   │   └— schema.txt
│   │   ├— modules/              # Core logic for v1
│   │   │   ├— create_schema.py
│   │   │   ├— gemini_chat.py
│   │   │   └— generate_webpage.py
│   │   ├— __init__.py
│   │   ├— api.py                # Endpoint logic
│   │   └— dependences.py        # Dependencies for API logic
│   ├— v2/                       # API Version 2 (CSS generation)
│   │   ├— instructions/css.txt
│   │   ├— modules/
│   │   │   ├— gemini_chat.py
│   │   │   └— generate_css.py
│   │   ├— __init__.py
│   │   ├— api.py
│   │   └— dependences.py
│   ├— v3/                       # API Version 3 (Retro Webpage with GPT-4o)
│   │   ├— instructions/html.txt
│   │   ├— modules/generate_retro_website.py
│   │   ├— __init__.py
│   │   ├— api.py
│   │   └— dependences.py
│   ├— v4/                       # API Version 4 (Beta with CSS/HTML)
│   │   ├— instructions/css.txt
│   │   ├— modules/
│   │   │   ├— gemini_chat.py
│   │   │   └— generate_css.py
│   │   ├— __init__.py
│   │   ├— api.py
│   │   └— dependences.py
│   ├— endpoints/                # Shared endpoint handlers
│   │   ├— __init__.py
│   │   └— page.py
│   ├— __init__.py
│   ├— api.py                    # Router includes all versions
│   └— dependences.py
│— main.py                       # Application entry point
│— Procfile                      # Heroku deployment config
│— requirements.txt              # Python dependencies
│— .env                          # Environment variables
│— .gitignore                    # Files to ignore in Git
```

---

## **How to Run**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/neuro-nostalgia.git
cd neuro-nostalgia
```

### **2. Install Dependencies**
Ensure Python 3.8+ is installed. Run the following:
```bash
pip install -r requirements.txt
```

### **3. Set Environment Variables**
Create a `.env` file in the root directory:
```plaintext
api_key=YOUR_API_KEY
telegram_bot_token=YOUR_TELEGRAM_BOT_TOKEN
telegram_chat_id=YOUR_TELEGRAM_CHAT_ID
html_assistant_id=YOUR_ASSISTANT_ID  # GPT-4o Specific
```

### **4. Start the API**
Run the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

## **API Endpoints**

### **1. General Overview**
The API includes four versions, with endpoints accessible via versioned prefixes.

| **Version** | **Description**                      | **Endpoint**           |
|-------------|--------------------------------------|------------------------|
| **v1**      | Generate Schema + Webpage (Gemini)   | `/v1/generate`         |
| **v2**      | Generate CSS + HTML (Gemini)         | `/v2/generate`         |
| **v3**      | Generate Retro Website (GPT-4o)      | `/v3/generate`         |
| **v4**      | Generate Beta CSS/HTML (Gemini)      | `/v4/generate`         |
| **Page**    | Fetch Generated Webpage              | `/{page_id}`           |

---

### **2. Generate Endpoints**

#### **v1: Schema + Webpage**
- **URL:** `POST /v1/generate`
- **Parameters:**
  - `url` (str): Source URL for schema generation.
  - `model_name` (str): Default: `gemini-1.5-flash`.
  - `max_output_tokens` (int): Default: `8192`.
  - `creativity` (int): Creativity level from 0-100.
- **Response:**
  ```json
  {
      "url": "http://example.com/unique_page_id"
  }
  ```

#### **v2: CSS + HTML**
- **URL:** `POST /v2/generate`
- **Description:** Generates CSS for the webpage.

#### **v3: Retro Webpage**
- **URL:** `POST /v3/generate`
- **Description:** Fine-tuned webpage generation using GPT-4o.
- **Parameters:**
  - `accuracy` (int): Accuracy level for content.
  - `creativity` (int): Controls content style.

#### **v4: Beta CSS/HTML**
- **URL:** `POST /v4/generate`
- **Description:** Beta version supporting CSS enhancements.

---

### **3. Fetch Generated Webpages**
- **URL:** `GET /{page_id}`
- **Description:** Retrieves a generated webpage by its `page_id`.
- **Response:** Returns HTML content.

---

## **Dependencies**
- Requests
- Fastapi
- Uvicorn
- Python-dotenv
- Beautifulsoup4
- Google-generativeai
- Openai

---

## **Author**
dvolynov@gmail.com

For any issues, open a pull request or raise an issue.

---
