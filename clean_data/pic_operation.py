import os
import shutil


def move_pic(pic_ls, save_path):
    count = 0
    for item in pic_ls:
        count += 1
        filename, extension = os.path.splitext(os.path.basename(item))
        directory_name = os.path.dirname(item)
        parent_directory, directory_name = os.path.split(directory_name)
        subdirectory_name = os.path.basename(directory_name)
        new_filename = subdirectory_name + extension
        new_image_path = os.path.join(save_path, new_filename)
        shutil.copy(item, new_image_path)
        print(subdirectory_name)


def remove_pic(directory, filename):
    if not os.path.exists(directory):
        print(f"目录 '{directory}' 不存在.")
        return
    file_path = os.path.join(directory, filename)
    print(file_path)
    if os.path.exists(file_path):
        if file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            os.remove(file_path)
            print(f"已删除文件: {file_path}")
        else:
            print(f"文件 '{filename}' 不是图片文件.")
    else:
        print(f"文件 '{filename}' 不存在.")


def get_success_pic(directory):
    sub_folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            sub_folders.append(item)
    success_pic_list = []
    for item in sub_folders:
        item_path = os.path.join(directory, item + "/screenshot.png")
        split_result = item.split("-")
        if len(split_result) == 2:
            if os.path.exists(item_path) and item != "legal_pic" and split_result[1] == "200":
                success_pic_list.append(item_path)
    return success_pic_list


def get_manual_search_pic(base_path, file_path):
    pic_ls = []
    other_ls = {}
    with open(file_path, "r") as f:
        for item in f:
            item = item.strip().split(" ")
            pic_ls.append(os.path.join(base_path, item[0] + "-200/screenshot.png"))
            if len(item) == 2:
                other_ls[item[0]] = item[1]
    return pic_ls, other_ls


if __name__ == '__main__':
    pass
    # legal_ls = get_manual_search_pic("E:\\code\\dataset\\legal", "info/manual_search_legal.txt")
    # move_pic(legal_ls[0], "E:\\code\\dataset\\manual_search_legal")

    phishing_ls = get_manual_search_pic("E:\\code\\dataset\\phishing", "info/manual_search_phishing.txt")
    move_pic(phishing_ls[0], "E:\\code\\dataset\\manual_search_phishing")

