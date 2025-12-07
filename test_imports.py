try:
    import pandas as pd
    print("pandas imported")
    import numpy as np
    print("numpy imported")
    import sqlite3
    print("sqlite3 imported")
except Exception as e:
    print(f"Error: {e}")
