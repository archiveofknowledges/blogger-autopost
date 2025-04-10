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
        "Creating Reusable Components",
        "Top 5 React Projects for Beginners",
        "React vs. Vue: Key Differences Explained"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a React developer writing friendly blog posts for aspiring frontend developers. "
        f"Write a post on the topic: '{selected_topic}'. "
        "Use a casual, engaging tone like a Dev.to article. Vary sentence lengths and structure naturally. "
        "Use <h2> for title, <h3> for subheadings, and wrap all explanation text in <p> tags. "
        "Include one clean code block using <pre><code class='language-js'>...</code></pre>. "
        "Avoid any Markdown or backticks. Ensure output is valid HTML for Blogger."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You write helpful React tutorials for self-taught frontend learners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1600
        )

        content = response.choices[0].message.content.strip()

        if "<pre><code" in content:
            parts = content.split("<pre><code", 1)
            main = parts[0].strip()
            code = "<pre><code" + parts[1]
        else:
            main, code = content, ""

        return {
            "title": selected_topic,
            "content": main,
            "code": code,
            "category": "react",
            "tags": ["React", "JavaScript", "Frontend", "Web Development", "Tutorial"]
        }

    except Exception as e:
        return {
            "title": "React Post (Error)",
            "content": f"<p>⚠️ Failed to generate post due to: {e}</p>",
            "category": "react",
            "tags": ["react", "error"]
        }
