import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from currencies.functions_currencies import get_currencies

if __name__ == "__main__":
    get_currencies()
