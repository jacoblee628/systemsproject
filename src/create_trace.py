import pandas as pd

import read_write as rw

def create_trace(file_path):
    obs_srs = pd.read_csv(obs_srs_file_path)
    obs_srs_list = obs_srs["Formatted ID"].unique()
    active_prd = pd.read_csv(active_prd_path)
    active_prd_list = active_prd["ID"].unique()