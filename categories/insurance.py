# blogger-autopost/categories/insurance.py

def generate_insurance_post(post_data):
    title = f"Best {post_data['insurance_type']} Insurance Plans for 2025"
    
    # 보험 관련 긴 글 작성
    content = f"""
    ## Best {post_data['insurance_type']} Insurance Plans for 2025
    
    ### Why {post_data['insurance_type']} Insurance is Important
    {post_data['importance']}
    
    ### Top Insurance Plans for {post_data['insurance_type']} in 2025
    - **{post_data['insurance_plan_1_name']}:** {post_data['insurance_plan_1_features']}
    - **{post_data['insurance_plan_2_name']}:** {post_data['insurance_plan_2_features']}
    - **{post_data['insurance_plan_3_name']}:** {post_data['insurance_plan_3_features']}
    
    ### How to Choose the Right Insurance Plan
    {post_data['selection_tips']}
    
    ### Pros and Cons of {post_data['insurance_type']} Insurance
    {post_data['pros_and_cons']}
    
    ### Conclusion
    {post_data['conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "insurance",
        "tags": ["insurance", post_data['insurance_type']],
    }
    
    return post_content
