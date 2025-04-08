# blogger-autopost/categories/finance.py

def generate_finance_post(post_data):
    title = f"Best Investment Strategies for {post_data['target_group']} in 2025"
    
    # 재정 관련 긴 글 작성
    content = f"""
    ## Best Investment Strategies for {post_data['target_group']} in 2025
    
    ### Introduction
    {post_data['intro']}
    
    ### Top Investment Strategies
    - **{post_data['strategy_1_name']}:** {post_data['strategy_1_details']}
    - **{post_data['strategy_2_name']}:** {post_data['strategy_2_details']}
    - **{post_data['strategy_3_name']}:** {post_data['strategy_3_details']}
    
    ### How to Start Investing
    {post_data['investment_tips']}
    
    ### Risks and Rewards of Investing
    {post_data['risks_and_rewards']}
    
    ### Conclusion
    {post_data['conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "finance",
        "tags": ["finance", post_data['target_group']],
    }
    
    return post_content
