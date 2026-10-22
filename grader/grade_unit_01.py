#!/usr/bin/env python3
"""Grade only Unit 01 Python files changed in a pull request.

Always execute this script from the trusted base-branch checkout, NOT from
the untrusted student branch. The runner has no write permissions.
"""
from __future__ import annotations
import ast
import os
from pathlib import Path
import re
import subprocess
import sys

UNIT="units/01-how-programs-work/practice"
CASES={
  "01-first-message": "Welcome to Computer Science I",
  "02-startup-sequence": "Booting...\nChecking sensors...\nReady.",
  "03-fix-the-messages": "Debugging in progress\nProblem solved",
  "04-robotics-status": "Wagner Robotics\nSystem online\nReady to launch"
}
TOTAL_PER_TASK=5
PATH_RE=re.compile(r"^units/01-how-programs-work/practice/([^/]+)/main\.py$")
BANNED_MESSAGE="Program exceeded the allowed execution time."

def changed_paths(student:Path)->list[str]:
    output=subprocess.check_output(
       ["git","-C",str(student),"diff","--name-only","HEAD^1","HEAD"],
       text=True,timeout=15)
    return output.splitlines()

def grade(student:Path):
    paths=changed_paths(student)
    slugs=sorted({m.group(1) for path in paths if (m:=PATH_RE.fullmatch(path)) and m.group(1) in CASES})
    if not slugs:
       return [], "No Unit 01 Python practice files changed. No exercises have been graded."
    results=[]
    for slug in slugs:
       path=student/UNIT/slug/"main.py"
       expected=CASES[slug]
       if not path.is_file():
          results.append((slug,False,"Required main.py was not found"))
          continue
       if path.stat().st_size>20000:
          results.append((slug,False,"File is too large for this introductory exercise"))
          continue
       try:
          source=path.read_text(encoding="utf-8")
          # A unit project is expected to explain its purpose in a comment.
          if slug=="04-robotics-status":
             comments=[line.strip() for line in source.splitlines() if line.lstrip().startswith("#")]
             custom=[c for c in comments if c not in {
                 "# Write a three-line robotics status display.",
                 "# Include a comment explaining the purpose of your program."
             }]
             if not custom:
                 results.append((slug,False,"Add a comment explaining the purpose of the script"))
                 continue
          completed=subprocess.run(
             [sys.executable,"-I",str(path)],text=True,capture_output=True,
             stdin=subprocess.DEVNULL,timeout=5,cwd=student,
             env={"PYTHONIOENCODING":"utf-8","PYTHONUNBUFFERED":"1"})
          if completed.returncode!=0:
             tail=completed.stderr.strip().splitlines()
             detail=(tail[-1] if tail else f"Python exited with code {completed.returncode}")
             results.append((slug,False,detail[:300]))
             continue
          output=completed.stdout.replace("\r\n","\n")
          if output.endswith("\n"):output=output[:-1]
          if output==expected:
             results.append((slug,True,"Output matches the requirements"))
          else:
             if len(output)>250:output=output[:250]+"..."
             results.append((slug,False,f"Expected {expected!r}; received {output!r}"))
       except subprocess.TimeoutExpired:
          results.append((slug,False,BANNED_MESSAGE))
       except Exception as exc:
          results.append((slug,False,f"{type(exc).__name__}: {str(exc)[:200]}"))
    earned=sum(TOTAL_PER_TASK for _,ok,_ in results if ok)
    maxpts=TOTAL_PER_TASK*len(results)
    lines=["## Unit 01 — Python Practice Results","","| Exercise | Result | Points |","|---|---|---:|"]
    for slug,passed,detail in results:
       lines.append(f"| `{slug}` | {'Passed' if passed else 'Needs revision'} | {TOTAL_PER_TASK if passed else 0}/{TOTAL_PER_TASK} |")
    lines.extend(["",f"**This submission: {earned}/{maxpts} points**",
     "",f"Only the **{len(results)} changed exercise(s)** were graded. Unchanged exercises are not zeros.","",
     "### Feedback",""])
    for slug,passed,detail in results:
       safe_detail=detail.replace("|","/").replace("\n"," ")
       lines.append(f"- **{slug}:** {safe_detail}")
    return results,"\n".join(lines)+"\n"

def main():
    student=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path("student").resolve()
    if not student.is_dir():
       raise SystemExit("Student checkout not found")
    results,report=grade(student)
    print(report)
    summary=os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
       with open(summary,"a",encoding="utf-8") as handle:handle.write(report)
    if any(not passed for _,passed,_ in results):
       raise SystemExit(1)

if __name__=="__main__":
    main()
