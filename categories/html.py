import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
    topics = [
        "Creating a Basic HTML Document",
        "Understanding HTML Headings and Paragraphs",
        "Working with Images in HTML",
        "Creating Lists and Tables in HTML",
        "Building Forms with Input Fields",
        "Using Links and Anchor Tags",
        "Understanding HTML Semantics",
        "Embedding Videos and Media",
        "Structuring Web Pages with HTML5 Elements",
        "Best Practices for Accessible HTML"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a friendly and knowledgeable HTML tutor writing a casual, friendly blog post on the topic: '{selected_topic}'. "
        "Use clean HTML only—no markdown, no triple backticks. "
        "Structure with <h2> for the title, <h3> for sections, and <p> for paragraphs. "
        "Include a clearly separated code example in a <pre><code class='language-html'>...</code></pre> block. "
        "Use a tone that feels natural and helpful, as if explaining to a beginner on a tech forum."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a casual HTML tutor writing easy-to-read HTML tutorials for beginners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1500
        )

        full_content = response.choices[0].message.content.strip()

        if "<pre><code" in full_content:
            parts = full_content.split("<pre><code", 1)
            content = parts[0].strip()
            code_block = "<pre><code" + parts[1]
        else:
            content = full_content
            code_block = ""

        return {
            "title": selected_topic,
            "content": content,
            "code": code_block,
            "category": "html",
            "tags": ["html", "web development", "frontend", "beginner", "tutorial"]
        }

    except Exception as e:
        print(f"❌ Error generating html post: {e}")
        return None
