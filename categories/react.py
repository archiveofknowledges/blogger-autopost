import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_react_post():
    # ✅ 다양한 React 주제 리스트
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
        f"You are a React instructor. Write a detailed React tutorial blog post on the topic: '{selected_topic}'. "
        "Use only HTML tags. DO NOT use Markdown or triple backticks. "
        "Use <h2> for the main title, <h3> for section headings, and wrap all explanation text in <p> tags. "
        "Include one <pre><code class='language-js'>...</code></pre> code block for example. "
        "Make sure the output is clean HTML that can be directly used in a Blogger post."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
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

    post = {
        "title": selected_topic,
        "content": content,
        "code": code_block,
        "category": "react",
        "tags": ["React", "JavaScript", "Frontend", "Web Development", "Hooks"]
    }
    return post
