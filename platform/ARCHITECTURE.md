# Classroom Platform — Authentication, Progress, Dashboard & Journals

**Status: design proposal.** The student login, student database, GitHub write-back and teacher dashboard below are **not deployed**. This document intentionally contains no real student identities, login credentials or private records.

## Recommendation

Use **Supabase (managed PostgreSQL + Auth + Row Level Security)** for student/classroom records, with **GitHub as the canonical code/version history** and `www.mswhitby.com` as the student UI.

### Why Supabase instead of Firebase?

Both support GitHub sign-in and fine-grained access rules. Firebase/Firestore is compelling for simple document-oriented real-time apps. A classroom system needs many related objects—**students → class periods → topics → attempts → revisions → mastery evidence → journal weeks**—and instructor queries that compare them. PostgreSQL relations, constraints and SQL grouping are a natural fit. Supabase's RLS controls access to individual records.

Do **not** put private student data in the public repository or in public JavaScript bundles. The existing public source code and lesson content can remain on GitHub.

## Proposed architecture

```text
www.mswhitby.com
├── Guided lessons    → public curriculum and in-browser Python
├── Challenge bank    → public problems and public-example checks
├── My Work           → authenticated resume, saved revisions, PR status
├── Weekly Journals   → authenticated, private student writing
└── Teacher Dashboard → authorized teachers only
         │
         ├── Supabase Auth (GitHub OAuth provider) → signed-in identity
         ├── Supabase Postgres + Row Level Security
         │    ├── sections / enrollments / profiles
         │    ├── lesson and challenge attempts / mastery evidence
         │    ├── journals / teacher feedback
         │    └── minimal engagement events
         └── trusted backend / Edge Functions
              ├── GitHub App tokens (never sent to browser)
              ├── GitHub fork/branch/code reads and writes
              ├── commits + PR create/update
              └── signed GitHub webhook ingestion / verified grades
                       │
                       └── GitHub Actions autograders + commit history
```

**Current implementation:** only public lesson/challenge pages, browser-local drafts, manual PR submission, and GitHub Actions grading exist. Do not put an inactive/fake login button on the student page.

## Github login is not the same as GitHub write permissions

1. **Sign in with GitHub** identifies the student for their private profile, journals and progress. Supabase Auth can support GitHub OAuth when a GitHub OAuth application, project credentials and callback URLs are configured.
2. **Grant course app access to the student's GitHub repository** separately. A GitHub App, with explicit authorization/installation and narrow repository permissions, would retrieve and update files. OAuth sign-in alone must not be treated as permission to modify arbitrary GitHub repositories.
3. Use the student's immutable GitHub **numeric user ID** rather than their changeable username as the stable external identity.
4. On every **Resume**, fetch the chosen file by repository + branch + path from GitHub, then load that content and its blob SHA. Offer an explicit choice if a browser draft differs from the GitHub version.
5. On **Save to GitHub**, write a new commit on a student-owned branch or fork with an optimistic SHA check; if the file changed elsewhere, show a conflict rather than overwriting it. Store only pointers and derived evidence in Supabase.
6. On **Submit**, create a PR if one does not exist for that unit/assignment and student branch; otherwise commit to its existing open branch. Provide the PR link and grader status. Keep an immutable pointer to every attempted commit.
7. Provide **My Work** organized by topic, activity and revision date. Students own their fork and can continue after the course; the teacher dashboard can inspect submitted commits without overriding student files.

The organization/fork permission workflow must be piloted with a teacher test account and a genuine student fork before broad use. GitHub App installation is a deliberate user action, not an automatic silent grant.

## Data model proposal (private Supabase project)

| Table | Purpose | Key fields |
|---|---|---|
| `profiles` | App account, linked GitHub identity | user UUID, GitHub numeric ID, GitHub login, role display |
| `sections` | Your class periods/cohorts | section UUID, course, term |
| `enrollments` | Student belongs to section | section UUID, user UUID, enrolled date |
| `teacher_section_grants` | Server-assigned teacher access | teacher UUID, section UUID |
| `topics` | Stable topic vocabulary | topic key, label, parent topic |
| `activities` | Stable lesson or challenge bank IDs | activity ID, type, topic tags, version |
| `assignments` / `assignment_items` | Optional weekly schedules and context-dependent points | section ID, activity ID, difficulty at assignment, points |
| `code_submissions` | Immutable links to student GitHub code | student, activity, repo, path, branch, commit SHA, PR number, time |
| `grading_evidence` | Server-verified results from GitHub | submission, topic, difficulty snapshot, points earned/possible, test version |
| `mastery_summaries` | Derived topic-level evidence | student, topic, current mastery estimate, last demonstration |
| `study_events` | Minimally necessary usage events | student, activity, event type, timestamp |
| `journal_prompts` | Instructor-issued reflection questions | section, week, questions, due |
| `journal_entries` | Student drafts and submissions, private | student, prompt, response fields, submitted timestamp |
| `journal_feedback` | Teacher feedback and status | entry, teacher, feedback, reviewed timestamp |

**Mastery must be derived from evidence**, not controlled by students themselves. A lesson check indicates practice; a verified independent challenge is stronger mastery evidence. Difficulty belongs to an assignment/evidence snapshot, because today's Hard question could be Easy later.

## Access controls (required, not optional)

- Turn on **Row Level Security** for every table containing student data.
- Student can view/edit **their own unfinished journal** and their own personal data/drafts, but cannot grant themselves teacher access, write verified grades, or modify another student's records.
- A teacher can read only their assigned sections; teacher grants and verified scores are written via a trusted server/admin process.
- Private service keys, GitHub App private keys, OAuth client secrets and webhook signing secrets stay **server-side**, never in GitHub Pages, `docs/`, localStorage or a public repository.
- The frontend Supabase public/publishable key is *not* a secret; secure RLS policies are the protection. Public access should default to deny for journals, rosters and grades.
- Test cross-student, cross-section and unauthorized teacher access with accounts that have no privileges before publishing student records.
- Avoid collecting precise location, invasive behavioral analytics, unnecessary personal details, or a student browsing history.
- Verify district approval, student privacy requirements, record retention and deletion rules **before** storing real class rosters, journals and grades in an external cloud provider. Public student GitHub code and usernames can reveal associations: provide a district-approved privacy plan.

## Student portal

**My Work:** dashboard of assigned and chosen activities, editor drafts, most recent GitHub commit and PR, resume previous code, recent automatic feedback. Treat unsent browser code as unsynced and visibly label it.

**Lessons / Challenges:** both available. A student may demonstrate competence through challenges or return to guided lessons. Track practice separately from assessed mastery.

**Weekly Journals:** instead of editing GitHub Pages, students get one private journal form per week (for example: what I built, problem I solved, where I got stuck, how I debugged, next goal). Allow Markdown, autosave drafts, revise until submitting, and a clear timestamp and teacher feedback. Do not ask students to put private reflections in public GitHub files.

## Teacher dashboard — proposed screens

1. **Class overview:** select period and date window; completion, submission status, unread journals, intervention indicators.
2. **Mastery matrix:** students × topics (e.g., variables, functions, Boolean logic, conditionals, loops, strings, lists, dictionaries). Show evidence count, last independent challenge, and difficulty distribution.
3. **Individual student:** activity history, revisions, grader results, GitHub code viewer, diffs between commits, notes, private journal responses.
4. **Assignment / challenge analytics:** attempted, passed, revision count, common error messages, topic-level obstacles, distribution by assigned difficulty.
5. **Engagement:** active days, distinct exercises attempted, run/check counts, submission activity. Do not equate page-open minutes or sheer click counts with learning.
6. **Journal inbox:** week, section, submitted/draft/missing, unread, teacher reply, export for private district records where permitted.

## Suggested delivery order

1. **District review and provider/network tests.** Confirm students can reach GitHub OAuth redirect and the Supabase project endpoints at school; an approved website alone does not mean all necessary subdomains are unblocked.
2. **Supabase project + GitHub sign-in.** Set up OAuth credentials/allowed redirects and **test RLS** with two student accounts and a teacher account.
3. **Private journals first.** This replaces parsing 140 personal journal pages and proves authentication, roster access and teacher permissions in a controlled workflow.
4. **My Work / GitHub integration.** Configure a GitHub App; pilot on one test student fork. Build Save/Resume/Submit and conflict handling.
5. **Verified grading ingestion + teacher analytics.** Consume signed GitHub events and trusted grade summaries. Derive mastery evidence and dashboards.
6. **Extend other languages:** Python first, then Java, JavaScript, React and C# with language-specific runners/checkers.

**No live Supabase account, OAuth callback, token, class roster or journal table has been created here.** These require explicit service setup and approved credentials.
