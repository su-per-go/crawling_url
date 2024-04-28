import csv
import os
import json
import pandas as pd

from crawling import DRIVER_PATH, WebPageAnalyzer, save_url_info


def loop():
    root_dir = "e:/code/dataset/legal_back_2/"
    df = pd.read_csv("domain/top-100000-domains.csv")
    url_ls = df.iloc[:, 0].tolist()[::-1]
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
        state_code, redirect, login_url = analyzer.analyze_page("https://" + url_ls[the_breakpoint["read_num"]+20000] + "/",
                                                                root_dir,
                                                                the_breakpoint["save_num"])

        print("第" + str(the_breakpoint["save_num"]) + "个", state_code, the_breakpoint["read_num"], "普通界面")
        save_url_info(root_dir + "url_info.csv", "https://" + url_ls[the_breakpoint["read_num"]+20000] + "/",
                      the_breakpoint["save_num"], the_breakpoint["read_num"], state_code, redirect)
        if login_url:
            the_breakpoint["save_num"] += 1
            state_code, redirect, _ = analyzer.analyze_page(login_url, root_dir, the_breakpoint["save_num"])
            save_url_info(root_dir + "url_info.csv", login_url, the_breakpoint["save_num"], the_breakpoint["read_num"],
                          state_code, redirect, login=True)
            print("第" + str(the_breakpoint["save_num"]) + "个", state_code, the_breakpoint["read_num"], "登录界面")

        the_breakpoint["read_num"] += 1
        the_breakpoint["save_num"] += 1

        with open(root_dir + "breakpoint_file.json", "w") as f:
            json.dump(the_breakpoint, f)


if __name__ == "__main__":
    loop()
