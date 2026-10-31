# Computer Science I — Python Foundations

A progressive, browser-friendly Python curriculum for Computer Science I.

The goal is to **learn one concept at a time**, practice it, and build on it in later units. Every lesson contains explanations, runnable examples, and small tasks that can be checked automatically. The curriculum draws inspiration from the *progressive teaching approach* of *Learn Python the Right Way*; its scenarios and explanations are original.

## Two learning tracks

### Current assignment — October 26 Python challenges

**[Open the interactive challenge lab on mswhitby.com](https://www.mswhitby.com/computer-science-1/challenges/)**

The [challenge bank](challenges/) contains 24 questions tagged by topic and categorized by difficulty, with 255 points in the [October 26 assignment](challenges/assignments/2026-10-26.json). The lab offers browser execution, public-example checking and optional skills explanations. **Official submissions still go to the [October 26 challenge repository](https://github.com/mswhitby/python_problems_20261026)** through the existing fork-and-PR workflow.

### Guided curriculum — Units 01–06

**[Open interactive Units 02–06 on mswhitby.com](https://www.mswhitby.com/computer-science-1/units/)**

There are **20 new lessons and independently checkable exercises** across Units 02–06, following the introductory [Unit 01](units/01-how-programs-work/README.md). Students can study lessons as needed rather than restarting from the beginning. The [lesson catalogs](units/) contain the topic explanations, starter Python files, three hints for each lesson, and the published public checks. The new [Unit 02–06 GitHub Actions grader](grader/grade_units_02_06.py) checks changed lesson files after a pull request. See [submission instructions](SUBMITTING.md).

This is a **separate track** from the reusable [challenge bank](challenges/). Both can support learning and assessment; your instructor decides what counts for credit.


### Interactive student site

**[Open Computer Science I Python practice on mswhitby.com](https://www.mswhitby.com/computer-science-1/)**

The student-facing app is published through the existing `mswhitby/classroom` website repository at `/computer-science-1/`. This avoids sending students to a blocked `github.io` URL. The lessons and grading code continue to live in this repository.

**Deployment note:** The app currently loads the Python browser runtime from `cdn.jsdelivr.net`; test **Run Code** on a district device before assigning it. If that CDN is blocked, host the runtime on the approved domain too.


## Curriculum roadmap

| Unit | Topic | Builds on |
|---|---|---|
| 01 | How programs work, output, execution order, debugging | No previous Python |
| 02 | Values, data types, variables, expressions | Output and execution |
| 03 | Functions, parameters, return values | Values and expressions |
| 04 | Comparisons and Boolean logic | Expressions and functions |
| 05 | Conditional execution | Boolean conditions |
| 06 | Iteration | Conditionals, tracing |
| 07 | Strings and string processing | Variables, loops, functions |
| 08 | Lists and collections | Loops and strings |
| 09 | Dictionaries and counting | Collections and loops |
| 10 | Cumulative challenges and projects | All prior units |

Units **01–06 are implemented**. Units 07–10 remain a provisional sequence, to be built after reviewing the first group.

## Student workflow (prototype)

1. Read [the unit lesson](units/01-how-programs-work/lesson.md).
2. Open the [guided Units 02–06](https://www.mswhitby.com/computer-science-1/units/) or [challenge lab](https://www.mswhitby.com/computer-science-1/challenges/) and select an exercise.
3. Write code, click **Run**, and see your output or error messages immediately.
4. Click **Check** to compare your output with the published requirements.
5. Code drafts and local checks save in the **current browser**.
6. To submit to GitHub for now, copy your code to the matching `main.py` (lessons) or `solution.py` (challenges) in the correct fork and open a pull request. [Submission guide](SUBMITTING.md).

**Automatic GitHub submissions are not implemented in the prototype.** That requires secure GitHub sign-in and a narrowly scoped backend/GitHub App. The browser app never asks for a password or access token.

## Instructor notes

- The [Unit 01 grader](grader/grade_unit_01.py) and [Units 02–06 grader](grader/grade_units_02_06.py) check changed lesson scripts on pull requests with read-only GitHub Actions workflows.
- Public browser checks are for learning; the GitHub workflow is the submission check.
- No student identity, gradebook, or credential data is stored in this repository.
- This repository is the course-content source. The existing `mswhitby/classroom` repository remains the site behind `mswhitby.com`; the site now includes separate interactive lesson and challenge areas.

## References

- [Learn Python the Right Way](https://learnpythontherightway.com/) — pedagogy inspiration
- [Python documentation](https://docs.python.org/3/)
- [Pyodide](https://pyodide.org/) — Python in the browser

## Shared Playground interface

Python now opens inside `mswhitby/playground`, alongside Game Programming, Mobile App & Web and UIL. This repository remains the authoring source for all 24 lessons, published examples, starters, hints, challenges and the Pyodide worker. The shared build packages these originals; no shortened replacement curriculum is introduced.

The old course home, lesson and challenge URLs redirect into the shared shell. Lesson/challenge hashes are carried across. Existing account IDs, `cs1:guided:v1:` and `cs1:challenges:2026-10-26:` draft/progress keys and activity IDs remain unchanged. Publish the corresponding shared Playground artifact before publishing these entry-page redirects.
