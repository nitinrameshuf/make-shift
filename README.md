def generate_hash(input_string):
    # Encode the input string to bytes
    input_bytes = input_string.encode('utf-8')
    
    # Generate the hash using SHA-256 algorithm
    hash_object = hashlib.sha256(input_bytes)
    
    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()
    
    return hash_hex
