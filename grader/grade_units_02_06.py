#!/usr/bin/env python3
"""Read-only PR grader for changed Unit 02–06 practice files.

Execute from the trusted base checkout. Tests in this public repository are
public; do not claim they are hidden or private.
"""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

def manifest():
    result = {}
    for unit in range(2, 7):
        data = json.loads((ROOT / "units" / ("catalog-" + str(unit) + ".json")).read_text())
        for item in data["lessons"]:
            folder, slug = item["id"].split("/")
            result["units/" + folder + "/practice/" + slug + "/main.py"] = item
    return result

def test_program(filename, record):
    if not filename.is_file() or filename.is_symlink():
        return False, "Missing regular main.py"
    if filename.stat().st_size > 30000:
        return False, "Source file is too large"
    code = filename.read_text(encoding="utf-8")
    expected_cases = record["cases"]
    if record["mode"] == "script":
        runner = code
    else:
        runner = (
            "import ast,json,io,contextlib\n"
            "source = " + repr(code) + "\n"
            "cases = " + repr(expected_cases) + "\n"
            "results=[]\n"
            "for item in cases:\n"
            "    try:\n"
            "        env={'__name__':'student'}\n"
            "        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):\n"
            "            exec(compile(source,'main.py','exec'),env)\n"
            "            if not callable(env.get('solution')): raise NameError('Define solution()')\n"
            "            value=eval(compile(ast.parse(item['call'],mode='eval'),'case','eval'),env)\n"
            "        expected=ast.literal_eval(item['expected'])\n"
            "        good=type(value) is type(expected) and value==expected\n"
            "        results.append({'pass':good,'actual':repr(value)[:150],'error':''})\n"
            "    except BaseException as e:\n"
            "        results.append({'pass':False,'actual':'','error':(type(e).__name__+': '+str(e))[:180]})\n"
            "print(json.dumps(results))\n"
        )
    try:
        completed = subprocess.run(
            [sys.executable, "-I", "-c", runner], cwd=str(filename.parent),
            capture_output=True, text=True, stdin=subprocess.DEVNULL,
            timeout=6, env={"PYTHONIOENCODING":"utf-8"}
        )
    except subprocess.TimeoutExpired:
        return False, "Execution exceeded 6 seconds"
    if completed.returncode:
        return False, (completed.stderr.splitlines() or ["Python error"])[-1][:180]
    if record["mode"] == "script":
        received = completed.stdout.replace("\r\n","\n").removesuffix("\n")
        expected = expected_cases[0]["expected"]
        return received == expected, ("Output matched" if received == expected else "Expected " + repr(expected) + "; got " + repr(received[:120]))
    try:
        results = json.loads(completed.stdout)
        if len(results) != len(expected_cases):
            return False, "Checker received incomplete results"
        passed = sum(bool(x.get("pass")) for x in results)
        misses = [str(i+1)+": "+(r["error"] or r["actual"]) for i,r in enumerate(results) if not r["pass"]]
        return passed == len(results), str(passed)+"/"+str(len(results))+" examples passed"+("; "+ "; ".join(misses[:3]) if misses else "")
    except (ValueError, KeyError, TypeError):
        return False, "Could not interpret checker output"

def main():
    student = Path(sys.argv[1]).resolve()
    known = manifest()
    change = subprocess.run(["git","-C",str(student),"diff","--name-only","HEAD^1","HEAD"],
        capture_output=True,text=True,check=True,timeout=15)
    paths = sorted(set(change.stdout.splitlines()) & set(known))
    rows = []
    for path in paths:
        item=known[path]
        ok,note=test_program(student/path,item)
        rows.append((item,ok,note))
    earned=sum(x["points"] for x,ok,_ in rows if ok)
    available=sum(x["points"] for x,ok,_ in rows)
    lines=["## Units 02–06 — Automated Practice Review","",
           "| Lesson | Result | Points |","|---|---|---:|"]
    for x,ok,note in rows:
        lines.append("| "+str(x["unit"])+"."+str(x["lesson"])+" "+x["title"]+
                     " | "+("Passed" if ok else "Needs revision")+
                     " | "+str(x["points"] if ok else 0)+"/"+str(x["points"])+" |")
    lines+=["","**Changed lessons: "+str(earned)+"/"+str(available)+" points**",
            "","Unchanged exercises are not counted as zero.","","### Feedback"]
    for x,ok,note in rows:
        lines.append("- **"+str(x["unit"])+"."+str(x["lesson"])+"** "+note.replace("|","/"))
    if not rows:
        lines.append("No Unit 02–06 practice files changed in this pull request.")
    report="\n".join(lines)+"\n"
    print(report)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a") as f:f.write(report)
    if any(not ok for _,ok,_ in rows):
        sys.exit(1)

if __name__=="__main__":
    main()
