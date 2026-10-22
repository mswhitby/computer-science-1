# Cost Watch — Computer Science I Platform

**Status: planning only. Checked October 22, 2026.**

This file is a checkpoint for future integrations. It does not actively monitor costs or create budgets. Ask for authorization before enabling any provider plan, add-on, paid runner, billing account, or usage-based service.

| Service / feature | Current status | Cost concern |
|---|---|---|
| Public `mswhitby/classroom` and Pages hosting | Live | GitHub Pages is available for public repositories on GitHub Free, within GitHub's limits. No new hosting subscription was added in this update. |
| Public-repository GitHub Actions grading | Already enabled | Standard GitHub-hosted runners are free and unlimited in public repositories; this does **not** automatically apply to private repositories. |
| Shared browser Python runtime | Existing and school-tested | Runs client-side in Pyodide. No separate metered grading server was enabled. |
| Purple, Dark, Dark Purple and Light themes | Live | Locally authored CSS/JS only: **no paid themes, fonts or providers**. |
| Supabase authentication, student records, journals, dashboard | **Not connected** | Supabase has a free tier (subject to limits) and Pro from **$25/month** at the current listed starting price. Free projects may pause after one week of inactivity. District approval and a privacy review are required first. |
| Firebase/Google Cloud Functions | **Not connected** | Firebase Cloud Functions requires the Blaze billing plan. Usage may fall within free quotas, but linking a billing account enables pay-as-you-go costs beyond allowances. |
| Private code execution runner (Judge0/container/Cloud Run) | **Not connected** | Requires separate infrastructure; can generate compute, storage, networking and security/ops expenses. Choose a budget, quotas and isolation before launch. |
| Private student GitHub repositories | **Not connected** | GitHub's Actions and storage pricing for private repos differs from public-repository free runners. Verify entitlements before provisioning for students. |
| Existing custom domain `mswhitby.com` | Already in use | Domain-registration and renewal costs are independent of these site changes; no new domain was purchased. |

## When to stop for an explicit cost decision

Pause and ask before:

1. Creating a paid Supabase organization, enabling Pro, custom domains or paid add-ons.
2. Enabling Firebase Blaze/Google Cloud Billing, Cloud Run, or metered student-submission grading.
3. Configuring private-repository CI that could exceed plan quotas.
4. Launching a third-party code sandbox requiring payment details or usage metering.
5. Adding commercial UI themes, fonts, third-party APIs, or software licenses.

Recommended first steps: use the current free website and public example checks; pilot login and secure storage only after provider and district reviews; budget and test the private grader on one account before provisioning for every student.

## Sources to verify before purchasing

- [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages)
- [GitHub hosted runner pricing for public repositories](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Supabase pricing](https://supabase.com/pricing)
- [Supabase billing quotas](https://supabase.com/docs/guides/platform/billing-on-supabase)
- [Firebase pricing plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans)

**No paid service has been provisioned for this UI update.** Never imply that a static-file deployment has started the private data or grading architecture.
