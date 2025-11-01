import sys, os

def add_project_root(project_name="mlops"):
    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.basename(current) == project_name or current == os.path.dirname(current):
            break
        current = os.path.dirname(current)
    sys.path.append(current)