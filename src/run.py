# TODO: When necessary args are decided, maybe write an argparser?

if __name__ == "__main__":
    """Code that's run when run.sh or python src/run.py is called"""
    print("Running script")
    
    v_v_test_report = "ER2228014 v51"
    version_num = "1.33"
    
    # TODO: remove these temp variables; only for development purposes
    prd_prefix = "US"
    srs_prefix = "TC"

    obs_srs_file_path = ""
    active_prd_path = ""

    
    # Load in rally export
    
    
    # Load previous traces (for backfilling if needed)
    trace_path = "../data/ER 2228015 v43 ATT1 Sapphire 1.33 Trace Matrix.xlsx"
    prev_trace_path = "../data/ER 2228015 v42 ATT1 Sapphire 1.32 Trace Matrix.xlsx"
    
    # 
    
    print("Script finished")