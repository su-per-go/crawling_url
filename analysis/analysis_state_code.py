import pandas as pd

base_path = "E:\\code\\dataset"
phishing_file = "phishing"
legal_crawling = "legal"


def read_state_code(path):
    df = pd.read_csv(path+"\\"+"url_info.csv")
    state_code_num = {}
    for state_code in df["state_code"]:
        if state_code == 600:
            state_code_num["其他"] = state_code_num.get("其他", 0) + 1
        else:
            state_code_num[str(state_code)] = state_code_num.get(str(state_code), 0) + 1
    return state_code_num


if __name__ == "__main__":
    legal_result = read_state_code(base_path + "\\" + legal_crawling)
    phishing_result = read_state_code(base_path + "\\"+phishing_file)
    ls = []
    print(list(legal_result.keys()))
    for key, value in phishing_result.items():
        the_dict = dict()
        the_dict["name"] = key
        the_dict["value"] = value
        ls.append(the_dict)
    print(ls)
    print(legal_result)
    print(phishing_result)

