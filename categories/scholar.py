# blogger-autopost/categories/scholar.py

def generate_scholar_post(post_data):
    title = f"{post_data['paper_title']} - A Study on {post_data['study_topic']}"
    
    # 학술적 내용의 긴 글 작성
    content = f"""
    ## {post_data['paper_title']} - A Study on {post_data['study_topic']}
    
    ### Introduction
    {post_data['intro']}
    
    ### Literature Review
    {post_data['literature_review']}
    
    ### Methodology
    {post_data['methodology']}
    
    ### Results and Discussion
    {post_data['results_and_discussion']}
    
    ### Conclusion and Future Work
    {post_data['conclusion']}
    
    ### References
    {post_data['references']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "scholar",
        "tags": ["scholar", post_data['study_topic']],
    }
    
    return post_content
