with open('build.sh', 'rb') as f:
    content = f.read()
new_content = content.replace(b'\r\n', b'\n')
with open('build.sh', 'wb') as f:
    f.write(new_content)
print("Forced LF on build.sh")
