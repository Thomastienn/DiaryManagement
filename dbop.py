import pickle, config

# cols_vals is a list of tuples
def update_database(db_dir: str, cols_vals: list) -> None:
    db = get_database(db_dir)
    for col_val in cols_vals:
        col, val = col_val
        db[col] = val        
    
    write_database(db, db_dir)

def update_relative_database(db_dir: str, cols_relvals: list) -> None:
    db = get_database(db_dir)
    for col_relval in cols_relvals:
        col, rel_val = col_relval
        db[col] += rel_val        

    write_database(db, db_dir)
    
def get_database(db_dir: str):
    db_file = open(db_dir, "rb")
    db = pickle.load(db_file)
    db_file.close
    
    return db

def write_database(db, db_dir: str) -> None:
    out_file = open(db_dir, "wb")
    pickle.dump(db, out_file)
    out_file.close()
    
def get_val(db_dir: str, col: str):
    db = get_database(db_dir)
    return db[col]
