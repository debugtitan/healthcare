import random
import string

def generate_blog_id():
    characters = string.ascii_letters + string.digits
    blog_id = ''.join(random.choice(characters) for _ in range(6))
    return blog_id