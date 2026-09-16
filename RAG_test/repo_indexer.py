import ast
import sys
from pathlib import Path
print(sys.executable)

def extract_function(file_path: Path):
    source=file_path.read_text("utf-8")
    tree = ast.parse(source)

    results=[]

    for node in ast.walk(tree):
        if isinstance(node,ast.FunctionDef):
            code=ast.get_source_segment(source,node)
            results.append({
                "name":node.name,
                "file":str(file_path),
                "start_line":node.lineno,
                "end_line":node.end_lineno,
                "code":code,
                "args":[arg.arg for arg in node.args.args],
                "docstring":ast.get_docstring(node)
            })
    return results

def index_repo(repo_path:str):
    repo=Path(repo_path)
    all_functions=[]

    for py_file in repo.rglob("*.py"):
        if ".venv" in py_file.parts:
            continue
        all_functions.extend(extract_function(py_file))
    return  all_functions

if __name__=="__main__":
    funcs = index_repo(r"E:\Indoor\PythonProject_learntest\Test_ex")
    print(f"抓取到{len(funcs)}个函数")
    for f in funcs:
        print(f["name"],f["file"],f["start_line"],f["end_line"])
