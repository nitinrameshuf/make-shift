text[:limit][:text[:limit].rfind('.')+1] if len(text) > limit and '.' in text[:limit] else text[:limit]
