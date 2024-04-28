from data_cleaning import cleaning_url_info
from pic_operation import remove_pic, get_success_pic


def read_txt(file_path):
    ls = []
    other_info = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            if len(line) == 2:
                ls.append(line[0])
                other_info.append(line[1])
            elif len(line) == 1:
                ls.append(line[0])
    return ls, other_info


if __name__ == '__main__':
    manual_legal_ls, _ = read_txt("info/manual_search_legal.txt")
    manual_phishing_ls, _ = read_txt("info/manual_search_phishing.txt")
    cleaning_url_info("E:/code/dataset/legal/", manual_legal_ls)
    cleaning_url_info("E:/code/dataset/phishing/", manual_phishing_ls)
