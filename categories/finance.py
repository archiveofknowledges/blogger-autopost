# blogger-autopost/categories/finance.py

def generate_finance_post(post_data):
    title = f"{post_data['topic_name']} - {post_data['topic_description']}"
    
    # 글을 길게 작성하는 방식
    content = f"""
    ## {post_data['topic_name']} - {post_data['topic_description']}
    
    ### Introduction
    {post_data['intro']}
    
    ### Detailed Analysis
    {post_data['detailed_analysis']}
    
    ### Key Takeaways
    {post_data['key_takeaways']}
    
    ### Conclusion
    {post_data['conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "finance",
        "tags": ["finance", post_data['topic_name']],
    }
    
    return post_content
