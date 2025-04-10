import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_scholar_post():
    topics = [
        "The impact of climate change on Arctic ecosystems",
        "Shakespeare's influence on modern literature",
        "Advancements in civil engineering materials",
        "The neuroscience of memory formation",
        "Evolution of classical music theory in the 20th century",
        "Economic effects of universal basic income",
        "Genetic engineering and CRISPR applications",
        "Architectural trends in postmodern urban design",
        "Sociological perspectives on digital identity",
        "Philosophical foundations of existential ethics",
        "Neural correlates of consciousness in sleep studies",
        "Historical context of political revolutions",
        "The ethics of artificial intelligence in modern warfare"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are an academic writer. Generate a well-structured blog post on the topic: '{selected_topic}'. "
        "Make it sound more natural, slightly informal, and human-written—like an insightful post you'd find on Medium. "
        "Avoid robotic or overly formal phrasing. Vary sentence lengths and paragraph sizes. "
        "Format in HTML only: use <h2> for the main title, <h3> for section headings, <p> for text, and <ul><li> for references. "
        "Include sections: Introduction, Literature Review, Methodology, Results and Discussion, Conclusion, and References. "
        "Finish with a note that cites general public sources like PubMed, JSTOR, or community forums."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert academic writer producing clear, human-like HTML blog posts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1800
        )

        content = response.choices[0].message.content.strip()

        # 출처 삽입
        content += "\n<p style=\"font-size: 0.9em; color: gray;\">Sources: Based on academic literature and community contributions (e.g., PubMed, JSTOR, academic blogs).</p>"

        post = {
            "title": selected_topic,
            "content": content,
            "category": "scholar",
            "tags": ["Scholarship", "Education", "Research", "Humanities", "Science"]
        }
        return post

    except Exception as e:
        print(f"❌ Error generating scholar post: {e}")
        return None
