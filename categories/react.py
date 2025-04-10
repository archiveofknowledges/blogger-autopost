import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_react_post():
    topics = [
        "Understanding JSX in React",
        "Props and State in Functional Components",
        "Handling Events in React",
        "Using useState and useEffect Hooks",
        "React Component Lifecycle",
        "Conditional Rendering in React",
        "Lists and Keys in React",
        "React Router Basics",
        "Lifting State Up in React",
        "Creating Reusable Components"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a React instructor writing for self-taught developers. Topic: '{selected_topic}'. "
        "Write in an informal and helpful tone, like a blog post you'd see on Dev.to or Medium. "
        "Vary paragraph lengths to sound more natural. Use only HTML tags: <h2> for title, <h3> for sections, <p> for text. "
        "Include one code example using <pre><code class='language-js'>...</code></pre>. "
        "Avoid Markdown and ensure formatting is Blogger-compatible."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a React developer creating friendly blog posts for new frontend learners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1600
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
            "category": "react",
            "tags": ["React", "JavaScript", "Frontend", "Web Development", "Hooks"]
        }

    except Exception as e:
        print(f"❌ Error generating react post: {e}")
        return None
