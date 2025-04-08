# categories/scholar.py

def generate_scholar_post(post_data):
    title = f"{post_data['paper_title']} - A Study on {post_data['study_topic']}"

    content = f"""
<h2>{post_data['paper_title']} - A Study on {post_data['study_topic']}</h2>

<h3>Introduction</h3>
<p>{post_data['intro']}</p>

<h3>Literature Review</h3>
<p>{post_data['literature_review']}</p>

<h3>Methodology</h3>
<p>{post_data['methodology']}</p>

<h3>Results and Discussion</h3>
<p>{post_data['results_and_discussion']}</p>

<h3>Conclusion and Future Work</h3>
<p>{post_data['conclusion']}</p>

<h3>References</h3>
<p>{post_data['references']}</p>

<p><em>Source: This summary is based on a combination of recent academic literature in the field of {post_data['study_topic']}. Please consult arXiv, Semantic Scholar, and Google Scholar for the original publications.</em></p>
"""

    tags = [
        "AI", "research", "deep learning", "machine learning", 
        post_data["study_topic"], "academic summary", "scholarly analysis"
    ]

    return {
        "title": title,
        "content": content,
        "category": "scholar",
        "tags": tags
    }
