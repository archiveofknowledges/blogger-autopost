# blogger-autopost/categories/minecraft.py

def generate_minecraft_post(post_data):
    title = f"Top Minecraft Mods, Servers, and Resource Packs for {post_data['year']}"
    
    # 마인크래프트 관련 긴 글 작성
    content = f"""
    ## Top Minecraft Mods, Servers, and Resource Packs for {post_data['year']}
    
    ### Introduction to Minecraft Mods, Servers, and Resource Packs
    {post_data['intro']}
    
    ### Top Mods for {post_data['year']}
    - **{post_data['mod_1_name']}:** {post_data['mod_1_features']}
    - **{post_data['mod_2_name']}:** {post_data['mod_2_features']}
    - **{post_data['mod_3_name']}:** {post_data['mod_3_features']}
    
    ### Best Minecraft Servers for {post_data['year']}
    - **{post_data['server_1_name']}:** {post_data['server_1_details']}
    - **{post_data['server_2_name']}:** {post_data['server_2_details']}
    
    ### Cool Resource Packs to Enhance Your Minecraft Experience
    - **{post_data['resource_pack_1_name']}:** {post_data['resource_pack_1_description']}
    - **{post_data['resource_pack_2_name']}:** {post_data['resource_pack_2_description']}
    
    ### Conclusion and Tips
    {post_data['conclusion_and_tips']}
    """
    
    post_content = {
        "title": title,
        "content": content,
        "category": "minecraft",
        "tags": ["minecraft", post_data['year']],
    }
    
    return post_content
