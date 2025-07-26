from yf.functions_yf import download_macro_symbols_all
from yf.functions_csv_to_table import import_all_csv_to_db
from yf.generate_indicators import generate_all_macro_features


download_macro_symbols_all()
import_all_csv_to_db()
generate_all_macro_features()



