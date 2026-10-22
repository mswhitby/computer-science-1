# Computer Science I — Python Foundations

A progressive, browser-friendly Python curriculum for Computer Science I.

The goal is to **learn one concept at a time**, practice it, and build on it in later units. Every lesson contains explanations, runnable examples, and small tasks that can be checked automatically. The curriculum draws inspiration from the *progressive teaching approach* of *Learn Python the Right Way*; its scenarios and explanations are original.

## Start here

**[Unit 01 — How Programs Work](units/01-how-programs-work/README.md)**

Unit 01 begins with writing instructions, using `print()`, following execution order, commenting code, and fixing simple syntax errors. No variables, loops, or custom functions are required.

### Interactive preview

The interactive Python practice app lives in [`docs/`](docs/). It runs Python in your browser and can check your practice output. Once GitHub Pages is enabled for this repository (source: `main`, folder `/docs`), its URL should be:

**https://mswhitby.github.io/computer-science-1/**

That URL is a *planned publication address*, not a confirmed live site. You can also preview locally by serving the `docs` directory over HTTP.

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

Only Unit 01 is implemented. Later units are a provisional sequence.

## Student workflow (prototype)

1. Read [the unit lesson](units/01-how-programs-work/lesson.md).
2. Open the practice app and select an exercise.
3. Write code, click **Run**, and see your output or error messages immediately.
4. Click **Check** to compare your output with the published requirements.
5. Code drafts and local checks save in the **current browser**.
6. To submit to GitHub for now, copy your code to the matching `main.py` in your fork and open a pull request. [Submission guide](SUBMITTING.md).

**Automatic GitHub submissions are not implemented in the prototype.** That requires secure GitHub sign-in and a narrowly scoped backend/GitHub App. The browser app never asks for a password or access token.

## Instructor notes

- The [autograder](grader/grade_unit_01.py) checks changed Unit 01 scripts on pull requests with a read-only GitHub Actions workflow.
- Public browser checks are for learning; the GitHub workflow is the submission check.
- No student identity, gradebook, or credential data is stored in this repository.
- This repository is the course-content source. The existing `mswhitby/classroom` repository remains the site behind `mswhitby.com`; **nothing was changed there**.

## References

- [Learn Python the Right Way](https://learnpythontherightway.com/) — pedagogy inspiration
- [Python documentation](https://docs.python.org/3/)
- [Pyodide](https://pyodide.org/) — Python in the browser
