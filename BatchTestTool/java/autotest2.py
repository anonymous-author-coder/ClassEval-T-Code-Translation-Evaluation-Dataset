import os
import shutil
import re


def extract_class_names(text_file):
    """从文本文件中提取 public class 后面的类名"""
    class_names = []
    with open(text_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 使用正则表达式提取 public class 后的类名
            match = re.search(r' class (\w+)', line)
            if match:
                class_names.append(match.group(1))  # 提取类名
    return class_names


def move_files(class_names, source_folder, target_folder):
    """根据类名移动文件，只有当 xxx 和 xxxTest 都存在时才移动"""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 记录未成功移动的文件
    not_moved_files = []

    # 过滤出有 Test 后缀和没有 Test 后缀的类名
    test_classes = {name for name in class_names if name.endswith("Test")}
    base_classes = {name for name in class_names if not name.endswith("Test")}

    # 查找每一个 base_class 是否存在对应的 Test 类
    for base_class in base_classes:
        corresponding_test_class = base_class + "Test"

        # 如果 base_class 和对应的 Test 类都存在于类名中，才移动文件
        if corresponding_test_class in test_classes:
            base_file_name = f"{base_class}.java"
            test_file_name = f"{corresponding_test_class}.java"

            base_source_path = os.path.join(source_folder, base_file_name)
            test_source_path = os.path.join(source_folder, test_file_name)

            base_target_path = os.path.join(target_folder, base_file_name)
            test_target_path = os.path.join(target_folder, test_file_name)

            # 移动基础类文件
            if os.path.exists(base_source_path):
                try:
                    shutil.move(base_source_path, base_target_path)
                    print(f"文件 {base_file_name} 已成功移动到 {target_folder}")
                except Exception as e:
                    print(f"移动文件 {base_file_name} 时发生错误: {e}")
                    not_moved_files.append(base_file_name)
            else:
                print(f"文件 {base_file_name} 不存在于源文件夹中: {source_folder}")
                not_moved_files.append(base_file_name)

            # 移动 Test 类文件
            if os.path.exists(test_source_path):
                try:
                    shutil.move(test_source_path, test_target_path)
                    print(f"文件 {test_file_name} 已成功移动到 {target_folder}")
                except Exception as e:
                    print(f"移动文件 {test_file_name} 时发生错误: {e}")
                    not_moved_files.append(test_file_name)
            else:
                print(f"文件 {test_file_name} 不存在于源文件夹中: {source_folder}")
                not_moved_files.append(test_file_name)

    # 输出没有移动成功的文件
    if not_moved_files:
        print("\n以下文件在 text 文件中存在，但未成功移动:")
        for file in not_moved_files:
            print(file)
    else:
        print("\n所有文件均已成功移动。")


# 指定text文档路径
text_file = r'D:\LLMS search\database\output\output.txt'  # 替换为实际的路径

# 指定源文件夹和目标文件夹路径
source_folder = r'D:\apache-maven-3.9.8-bin\untitled1\src\main\java\org\example'  # 替换为实际的路径
target_folder = r'D:\LLMS search\database\llms_code'  # 替换为实际的路径

# 从文本文件中提取类名
class_names = extract_class_names(text_file)

# 根据类名移动相应的文件，只有当 xxx 和 xxxTest 都存在时才移动
move_files(class_names, source_folder, target_folder)
