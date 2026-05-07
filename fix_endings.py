import os

def fix_line_endings(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    
    # Check for CRLF
    if b'\r\n' in content:
        print(f"Fixing CRLF in {filename}")
        new_content = content.replace(b'\r\n', b'\n')
        with open(filename, 'wb') as f:
            f.write(new_content)
        return True
    return False

files_to_fix = ['build.sh']
for f in files_to_fix:
    if os.path.exists(f):
        fix_line_endings(f)
    else:
        print(f"File {f} not found")
