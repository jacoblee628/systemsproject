# TODO: When necessary args are decided, maybe write an argparser?

if __name__ == "__main__":
    """Code that's run when run.sh or python src/run.py is called"""
    print("Running script")
    
    prd_prefix = "US"
    srs_prefix = "TC"

    obs_srs_file_path = ""
    obs_srs = pd.read_csv(obs_srs_file_path)
    obs_srs_list = obs_srs["Formatted ID"].unique()

    active_prd_path = ""
    active_prd = pd.read_csv(active_prd_path)
    active_prd_list = active_prd["ID"].unique()
    
    # Load trace
    trace_path = "../data/ER 2228015 v43 ATT1 Sapphire 1.33 Trace Matrix.xlsx"
    prev_trace_path = "../data/ER 2228015 v42 ATT1 Sapphire 1.32 Trace Matrix.xlsx"
    
    # 
    
    print("Script finished")