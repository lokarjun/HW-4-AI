import random
import string
import os

def random_text(length):
    """Generate random text of specified byte length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_file(filename, content):
    """Save content to a file"""
    with open(filename, 'w') as f:
        f.write(content)

def generate_inputs(folder="inputs", size_bytes=2_000_000):
    """Generate plain text, ASCII text, and Hexadecimal text"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 1. Plain text
    plain_text = random_text(size_bytes)
    save_file(os.path.join(folder, "plain_text.txt"), plain_text)

    # 2. ASCII code version
    ascii_code = ''.join([str(ord(c)).zfill(3) for c in plain_text])
    save_file(os.path.join(folder, "ascii_text.txt"), ascii_code)

    # 3. Hexadecimal version
    hex_text = ''.join(random.choices('0123456789abcdef', k=2 * size_bytes))
    save_file(os.path.join(folder, "hex_text.txt"), hex_text)

    print(f"Pre-generated files saved in '{folder}/'")

if __name__ == "__main__":
    generate_inputs()
