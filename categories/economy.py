# blogger-autopost/categories/economy.py

def generate_economy_post(post_data):
    title = f"{post_data['indicator_name']} - Economic Data for {post_data['country']} on {post_data['date']}"
    
    # 경제 지표 관련 긴 글 작성
    content = f"""
    ## {post_data['indicator_name']} - Economic Data for {post_data['country']} on {post_data['date']}
    
    ### Overview
    {post_data['overview']}
    
    ### Latest Data
    - **{post_data['indicator_name']}:** {post_data['indicator_value']}
    
    ### Impact of the Indicator on the Economy
    {post_data['impact_on_economy']}
    
    ### Conclusion
    {post_data['conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "economy",
        "tags": ["economy", post_data['indicator_name']],
    }
    
    return post_content
