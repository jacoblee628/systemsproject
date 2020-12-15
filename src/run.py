# TODO: When necessary args are decided, maybe write an argparser?

def run(params):
    """Code that's run when run.sh or python src/run.py is called"""
    print("Running script")
    
    v_v_test_report = "ER2228014 v51"
    version_num = "1.33"
    
    # TODO: remove these temp variables; only for development purposes
    prd_prefix = "US"
    srs_prefix = "TC"

    obs_srs_file_path = ""
    active_prd_path = ""
    
    # obs_srs = pd.read_csv(obs_srs_file_path)
    # obs_srs_list = obs_srs["Formatted ID"].unique()
    # active_prd = pd.read_csv(active_prd_path)
    # active_prd_list = active_prd["ID"].unique()

    # Load previous traces (for backfilling if needed)
    # trace_path = "../data/ER 2228015 v43 ATT1 Sapphire 1.33 Trace Matrix.xlsx"
    # prev_trace_path = "../data/ER 2228015 v42 ATT1 Sapphire 1.32 Trace Matrix.xlsx"
    
    # run "create_trace.create_trace()"
    
    print("Script finished")

if __name__ == "__main__":
    # TODO: Implement argparser and pass args in a dict here (for running via console)
    params = {}
    run(params)