import os

import pandas as pd
import random


def cleaning_url_info(file_path, manual_ls):
    df = pd.read_csv(file_path + "url_info.csv")
    df["success"] = 0
    drop_index = []
    for index, row in df.iterrows():
        if row["state_code"] == 600:
            drop_index.append(index)
        elif row["state_code"] == 200:
            request_info = file_path + str(row["num"]) + "-" + "200"
            try:
                if len(os.listdir(request_info)) == 5 and str(row["num"]) not in manual_ls:
                    df.at[index, 'success'] = 1
            except Exception as e:
                pass
    df = df.drop(drop_index)
    df = df.reset_index(drop=True)
    count = df['state_code'].value_counts()

    data_dict = dict(count)
    del data_dict[200]
    keys = list(data_dict.keys())
    weights = list(data_dict.values())
    for index, row in df.iterrows():
        if row["state_code"] == 200 and row["success"] == 0:
            # 根据权重随机选择一个键
            selected_key = random.choices(keys, weights=weights)[0]
            df.at[index, 'state_code'] = selected_key

    df.to_csv(file_path + "new_url_info.csv", index=False)
