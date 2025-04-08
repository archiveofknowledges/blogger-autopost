# blogger-autopost/categories/credit_cards.py

def generate_credit_card_post(post_data):
    title = f"Best Credit Cards for {post_data['target_group']} in 2025"
    
    # 신용카드 관련 긴 글 작성
    content = f"""
    ## {post_data['target_group']} - Best Credit Cards in 2025
    
    ### Introduction
    {post_data['intro']}
    
    ### Top Credit Cards for {post_data['target_group']}
    - **{post_data['card_1_name']}:** {post_data['card_1_features']}
    - **{post_data['card_2_name']}:** {post_data['card_2_features']}
    - **{post_data['card_3_name']}:** {post_data['card_3_features']}
    
    ### How to Choose the Right Credit Card
    {post_data['card_selection_tips']}
    
    ### Pros and Cons of Using Credit Cards
    {post_data['pros_and_cons']}
    
    ### Conclusion
    {post_data['conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "credit_cards",
        "tags": ["credit_cards", post_data['target_group']],
    }
    
    return post_content
