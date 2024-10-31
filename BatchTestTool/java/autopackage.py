import os

def add_package_statement(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 检查文件中是否已经存在 package 语句
    package_statement_exists = any(line.strip().startswith("package") for line in lines)

    if not package_statement_exists:
        # 在文件开头添加 package 语句
        lines.insert(0, "package org.example;\n")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print(f"Added package statement to: {file_path}")
    else:
        print(f"Package statement already exists in: {file_path}")

def process_directory(root_folder):
    # 遍历根目录及其所有子文件夹
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".java"):
                file_path = os.path.join(dirpath, filename)
                add_package_statement(file_path)

# 替换成你的大文件夹路径
root_directory = 'D:/apache-maven-3.9.8-bin/apache-maven-3.9.8\\lib/untitled5\\src\\main\\java\\org\\example'  # 将此路径替换为大文件夹的路径
process_directory(root_directory)