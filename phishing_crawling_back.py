import csv
import os
import json
from crawling import DRIVER_PATH, WebPageAnalyzer, save_url_info

def loop():
    root_dir = "e:/code/dataset/phishing_back/"
    with open("domain/verified_online.json", "r") as f:
        file = json.load(f)
    url_ls = []
    for i in file:
        url_ls.append(i["url"])
    url_ls = url_ls[::-1]
    driver_path = DRIVER_PATH
    analyzer = WebPageAnalyzer(driver_path)
    file_path = os.path.join(root_dir, "url_info.csv")
    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as f:
            head = ["num", "index", "request_url", "state_code", "response_url", "login_page", "time"]
            csv_writer = csv.writer(f)
            csv_writer.writerow(head)

    while True:
        with open(root_dir + "breakpoint_file.json", "r") as f:
            the_breakpoint = json.load(f)
        if the_breakpoint["read_num"] > len(url_ls):
            break
        state_code, redirect, login_url = analyzer.analyze_page(url_ls[the_breakpoint["read_num"]],
                                                                root_dir,
                                                                the_breakpoint["save_num"])

        print("第" + str(the_breakpoint["save_num"]) + "个", state_code, the_breakpoint["read_num"], "钓鱼页面")
        save_url_info(root_dir + "url_info.csv", url_ls[the_breakpoint["read_num"]],
                      the_breakpoint["save_num"], the_breakpoint["read_num"], state_code, redirect)
        the_breakpoint["read_num"] += 1
        the_breakpoint["save_num"] += 1

        with open(root_dir + "breakpoint_file.json", "w") as f:
            json.dump(the_breakpoint, f)


if __name__ == "__main__":
    loop()
