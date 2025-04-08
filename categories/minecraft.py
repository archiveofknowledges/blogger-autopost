# blogger-autopost/categories/minecraft.py

def generate_minecraft_post(post_data):
    title = f"Minecraft Server: {post_data['server_name']}"
    
    # 글을 길게 작성하는 방식 (서버 소개, 플레이 방법, 추천 모드 등)
    content = f"""
    ## Minecraft Server: {post_data['server_name']}
    
    ### Server Description
    {post_data['server_description']}
    
    ### How to Join
    {post_data['server_join_instructions']}
    
    ### Recommended Mods
    {post_data['recommended_mods']}
    
    ### Additional Resources
    {post_data['additional_resources']}
    
    ### Conclusion
    {post_data['server_conclusion']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "minecraft",
        "tags": ["minecraft", post_data['server_name']],
    }
    
    return post_content
