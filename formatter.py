import markdown

def format_post(content):
    """
    포스트의 내용을 포맷팅하는 함수
    markdown을 HTML로 변환
    """
    return markdown.markdown(content)
