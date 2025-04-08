# blogger-autopost/categories/economy.py

def generate_economy_post(post_data):
    title = f"Economic Indicator: {post_data['indicator_name']}"
    
    # 글을 길게 작성하는 방식 (예: 인용, 설명, 배경, 세부사항 등을 포함)
    content = f"""
    ## {post_data['indicator_name']} - {post_data['indicator_title']}
    
    ### Overview
    {post_data['indicator_summary']}
    
    ### Analysis
    {post_data['indicator_analysis']}
    
    ### Implications
    {post_data['indicator_implications']}
    
    ### Conclusion
    {post_data['indicator_conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "economy",
        "tags": ["economy", post_data['indicator_name']],
    }
    
    return post_content
