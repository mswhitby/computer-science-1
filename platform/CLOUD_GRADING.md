# Cloud Grading: Submit without a Pull Request

**Design proposal — not deployed.** This is the proposed successor to manually submitted GitHub pull requests. The existing challenge grader and Unit 01–06 GitHub Actions workflows remain operational until a secure replacement has been piloted.

## Goals

1. Keep **all attempts** for every student and every activity, including unsuccessful attempts and exceptions.
2. Award the **highest verified score** for the same activity in the same grading scope (e.g., weekly assignment or year-long challenge bank).
3. Execute official cases **only on a private, isolated grading service**. The browser can run public examples for practice.
4. Students can **resume their own GitHub code** and inspect prior revisions.
5. The teacher dashboard can inspect submitted code, revisions, score history, and mastery evidence, without using public student repositories as a gradebook.
6. Support both structured Units 01–06 and open challenge-bank questions from one grading API, then other languages.

## Submission flow

```text
Student's browser at www.mswhitby.com
    |
    +-- Run / Check examples
    |       -> local Pyodide, no official score
    |
    +-- Save to GitHub
    |       -> authenticated server saves to student's permitted repo
    |       -> new immutable Git commit; may remain a draft
    |
    +-- Submit for Grade (authenticated)
            -> validate student, enrollment, activity, rate limit
            -> snapshot exact source and/or verified Git commit SHA
            -> create immutable attempt (status: queued)
            -> enqueue grading job
                  |
                  v
           isolated sandbox runner
             private cases + evaluation rubric
             strict language/version, time/memory/output limits,
             no internet, no teacher/database tokens
                  |
                  v
           trusted result ingester
             validates worker identity + attempt ID + test version
             writes score, status, safe feedback, timestamps
             updates derived best-score/mastery records atomically
                  |
                  +-- Student: scored attempt + personal history
                  +-- Teacher: attempts, GitHub code, mastery matrix
```

**Supabase Edge Functions handle authentication, request validation, queue orchestration, and result ingestion.** They should not execute student Python/Java/C#/JavaScript directly. Current Supabase hosted Edge Functions have tight CPU limits and are not a specialized sandbox. Choose a protected code runner (e.g., isolated containers or a carefully secured Judge0 deployment), with the runner itself having **no database secret, GitHub secret or network access**.

### A reliable Submit sequence

- Verify Supabase JWT and check the student's permitted course/section and activity ID on the server.
- Resolve the student's GitHub identity **and GitHub App installation permission** separately: login alone is not permission to write repositories.
- Create a GitHub commit containing the submitted source or first record an immutable versioned source snapshot with the student's explicit consent. Use the submitted content's SHA-256 and Git commit SHA to link the exact source to the grade.
- Assign a server-generated attempt UUID and an idempotency key. Duplicate clicks or job retries must not create duplicate graded attempts.
- Persist an immutable queued attempt and return `202 Accepted` with `attempt_id` and a status URL.
- Grade asynchronously against a **private test bundle** versioned by problem ID and rubric version.
- Store all results. An error or timeout is still an attempt (with zero earned points and a safe error category).
- Allow subsequent commits/submissions, with each revision preserving its own score.

## Minimum private tables

| Table | Fields / responsibility |
|---|---|
| `activities` | stable activity ID, version, topics, language, source repository (public prompts only) |
| `grading_scopes` | course / assignment / grading-period context (can be open-ended challenge bank) |
| `grading_rubrics` | stable rubric ID + version, points possible, test-set reference **not accessible to the client** |
| `grade_attempts` | attempt UUID, student UUID, activity ID, grading scope ID, submitted at, GitHub repo/path/commit, source hash, status, safe feedback |
| `grade_results` | attempt ID, rubric version, passed/total, points earned/possible, verified at, worker result signature |
| `best_scores` | materialized current best per **student + activity + scope + rubric version**, including winning attempt ID |
| `topic_evidence` | derived records from scored attempts: topic, graded difficulty snapshot, independence/revision indicators |
| `grading_events` | internal job lifecycle and failure audit log; no secrets or private test inputs in student-visible events |

Mastery scores and grading policies can evolve without deleting attempts. A difficulty rating is recorded **at the time of the attempt**, not permanently fixed to the challenge-bank folder.

## Best score policy

Use **best verified attempt**, not most recent attempt. Failed, timed-out and syntax-error attempts remain in the timeline but do not reduce the awarded score. A tie can use the earlier completed best attempt or latest to show improvement, according to the teacher's preference.

For the same student, activity, scope and version:

```sql
-- Conceptual query: a trusted backend creates or refreshes the summary.
SELECT student_id, activity_id, grading_scope_id, rubric_version,
       MAX(points_earned) AS awarded_points
FROM verified_grading_results
GROUP BY student_id, activity_id, grading_scope_id, rubric_version;
```

The source of truth is the immutable attempt and result history. Use a database transaction / atomic UPSERT when maintaining a `best_scores` cache; do **not** trust a client-provided score.

**Rubric changes:** if a new rubric changes point values or test cases, either (a) keep separate rubric-version results or (b) regrade all applicable saved submissions using the new rubric. Never compare scores across incompatible rubrics as though they were equivalent.

**Multiple possible grading paths:** a student might show skill through lessons, independent challenges, or both. Dashboard mastery can draw from all verified evidence, while a grade for a specific activity/scope still uses that activity's highest attempt. Practicing a lesson is a weaker mastery signal than solving an unfamiliar challenge independently.

## Concealing official tests and solutions

Moving grading to the server **prevents browsing current official grading cases from the public student repository**, but only if cases, reference solutions, grader credentials, and worker logs are never published there.

- Keep prompts, official starter code, topics and **public examples** in `computer-science-1` and other public content repositories.
- Keep **private grading cases, expected answers and reference implementations** in a private repository and/or protected backend storage. The grading runner has short-lived, read-only access to required cases.
- Keep source and expected values for **secret** tests out of the browser, the Supabase browser client, publicly accessible CI logs, and feedback.
- Feedback can describe a category (wrong return type, missed boundary, incorrect ordering) without giving away actual private inputs and expected outputs.
- Rate-limit costly/unlimited grading submissions to discourage brute-force probing, while allowing as many drafts and local public-example checks as students need.
- **Important migration issue:** the existing October 26 repository's `tests` and `solutions` branches have been publicly accessible. Deleting those branches cannot guarantee copies or Git history become inaccessible. Treat previously exposed cases as compromised and write/rotate fresh **private** official tests; do not simply reuse public cases and label them hidden.
- **Another important issue:** standard forks of public GitHub repositories are also public. Students can read each other's submitted code in those forks. For privacy / reduced copying, use distinct **private student repositories** rather than public forks, preferably created from a clean public template or a new independent repo with the GitHub App explicitly granted access. A private repository is not the same thing as a private fork of a public repository.
- Even with private code/test storage, no automatic grader can fully prevent copied answers or answer-sharing. Discuss expectations and use process evidence, explanation, and occasional live debugging exercises.

## Student code history: save, resume, submit

Each student's own GitHub repository is their **canonical code archive**.

- **Save draft:** create/update the student's own GitHub file; store a commit ID in their profile. Do not create a graded attempt.
- **Resume:** read the latest permitted GitHub file, load code into the editor, and offer a conflict choice if its content differs from the local browser draft.
- **Submit:** snapshot the exact graded version of the source. Store the commit SHA and grading attempt ID, not just a mutable branch name.
- **History:** show each Git commit and each graded attempt together. The student can restore old code, then make a new commit; previously earned credit is unaffected.
- The student should have lasting access to their private repository or an export mechanism when they leave the class. If the repo is teacher/organization owned, agree on an end-of-course handoff policy.

## API contract (initial proposal)

| Route | Auth | Request | Result |
|---|---|---|---|
| `POST /grade/submit` | student | activity ID, scope ID, submitted revision/commit, idempotency key | attempt ID and queued status |
| `GET /grade/attempts/:id` | owner / assigned teacher | attempt ID | status and safe feedback |
| `GET /grade/best?scope=...` | owner / assigned teacher | scope | best-score snapshots |
| `POST /code/save` | student | activity ID, branch + code, expected blob SHA | committed SHA or conflict |
| `GET /code/resume` | student / teacher view | activity ID | latest permitted commit and source |
| `POST /grade/worker-result` | worker only | signed attempt/rubric/job result | verified scores committed |

Server must derive **student identity and access rights** from the authenticated session. Never trust user IDs, grades, arbitrary repository destinations or rubric versions in browser request bodies.

## Teacher dashboard integration

- Show **highest grade**, current-attempt grade, total attempts, date first attempted, most recent practice/grade, and what was learned.
- Select a student to inspect GitHub source **at the exact graded commit**. Provide revision history, safe failure categories, and topic/evidence trends.
- Preserve both successful and unsuccessful attempts. Don't display a record of failure as a permanent zero when a student has since passed.
- Journal data remains private in Supabase with role-based access and is not placed in git.

## Pilot plan

1. District approves student data provider/retention and network access; create private backend project with RLS.
2. Configure GitHub OAuth sign-in and separately authorize a GitHub App for a private student test repository.
3. Create the attempt tables and `best_scores` transaction; test access with two students and one teacher.
4. Run *one* low-risk Python problem through an isolated execution service using fresh private cases.
5. Submit four revisions (5/25, 15/25, 10/25, 25/25) and verify four immutable attempts + final 25/25.
6. Test duplicate clicks, runner timeout, student switching accounts, denied foreign records, code resume/version conflict, and grader retry.
7. Only then replace weekly PR submission for students; retain the working GitHub grader as a fallback.

## Official references

- Supabase [Edge Functions](https://supabase.com/docs/guides/functions) and [CPU resource limits](https://supabase.com/docs/guides/troubleshooting/edge-function-cpu-limits)
- Supabase [GitHub OAuth](https://supabase.com/docs/guides/auth/social-login/auth-github)
- GitHub [fork visibility](https://docs.github.com/en/pull-requests/reference/forks)
- [Judge0](https://github.com/judge0/judge0) sandbox execution
