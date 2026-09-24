# Code Ring: action guide

81 coding prompts, from scope to release review.

9 source categories across 11 navigation pages including Home. Home has at most 8 controls; action folders have at most 9. When needed, More workflows opens the remaining categories without removing any action.

Text actions wait one second, then paste a prompt without pressing Enter. Windows shortcuts act immediately. Folder navigation is supplied by Logi Options+.

## Home

![Code Ring / Home](previews/code-ring-home.svg)

### 1. Plan & Scope

Open [Plan & Scope](previews/code-ring-plan-scope.svg).

### 2. Build & Fix

Open [Build & Fix](previews/code-ring-build-fix.svg).

### 3. Debug & Trace

Open [Debug & Trace](previews/code-ring-debug-trace.svg).

### 4. Context & Agent Ops

Open [Context & Agent Ops](previews/code-ring-context-agent-ops.svg).

### 5. Git & PR

Open [Git & PR](previews/code-ring-git-pr.svg).

### 6. Ship & Harden

Open [Ship & Harden](previews/code-ring-ship-harden.svg).

### 7. Explain & Learn

Open [Explain & Learn](previews/code-ring-explain-learn.svg).

### 8. More workflows

Open [More workflows](previews/code-ring-home-more.svg).

## Plan & Scope

![Code Ring / Plan & Scope](previews/code-ring-plan-scope.svg)

### 1. Scope Questions

Ask me the questions that would reshape your plan, as a numbered multiple-choice list, because every question I answer is an assumption you no longer have to invent. Check the repo first and skip anything it already answers. Cap it at the questions that actually change the plan and ask about nothing else. Do not plan or code yet; stop and wait for my answers.

### 2. Write Plan

Write a plan document: goal, success criteria, non-goals, file-level tasks and the validation for each step. Verify existing paths; clearly label proposed new files. Save only the plan, report its location and stop before implementation.

### 3. Split Phases

Split this plan into numbered phases, each small enough to finish in one context window and each with an explicit completion condition, because a phase that outgrows its window is where instruction drift starts. Report the phase list and what each one leaves untouched, then stop.

### 4. Open Questions

List every question this plan still leaves open, ranked by how much damage a wrong guess would do, because the unresolved list is worth more than the confident parts. Check the repo for anything that already answers one, and say plainly where the data is insufficient instead of guessing. Change nothing else, and stop for my answers.

### 5. Compare Approaches

Compare the two most viable approaches on complexity, blast radius, testability, and cost to reverse, because a decision without a reversal cost is a guess. Recommend one, name the single deciding factor, and report what evidence would flip it. Write no code yet, leave the repo untouched, and stop.

### 6. Define Interfaces

Define the shapes first: data structures, interfaces, types, errors, and events, with usage examples you can run, because if the shapes are wrong nothing built on them can be right. Run one example to prove the shapes compile. Do not implement any behavior yet; stop for my approval, and change nothing else until the shapes are locked.

### 7. Risk Check

List the assumptions this plan rests on, ranked by risk, and for each one name the cheapest check that would prove or kill it, because an assumption nobody tested is a bug with a delay timer. Run the checks that cost nothing, report the output, change nothing else, and stop before acting on the rest.

### 8. Define Done

Define done before any code: the observable behaviors, the edge cases in scope, what is explicitly out of scope, and the exact command or check that proves each one, because acceptance criteria written afterwards always describe whatever got built. Write no code, and stop for approval.

### 9. Handoff Spec

Write a spec another assistant can execute without this chat: context, goal, constraints, ordered tasks, acceptance criteria and exact verification commands. Verify existing paths and label new ones as proposed. Save only the spec, report its location and stop.

## Build & Fix

![Code Ring / Build & Fix](previews/code-ring-build-fix.svg)

### 1. Implement Phase

Implement only the current phase of the plan, because scope that grows quietly is scope nobody reviewed. Follow the patterns already in this repo, leave unrelated code untouched, run the checks the plan names, and report the actual output plus every file you touched, and stop at the phase boundary.

### 2. Mark Todo

Insert an explicit TODO marker at every location you intend to change, and report the list with paths and line numbers, because I would rather correct your map than your diff. Write no implementation yet, touch nothing else, and stop until I confirm the markers are right.

### 3. Isolated Probe

Run a disposable implementation probe in a new isolated worktree or scratch directory. First verify the original worktree will remain untouched. Compare the result to the plan, document the assumptions that failed and show the probe diff. Do not merge, delete, or discard the probe without approval. Leave the original project unchanged.

### 4. Fix Error

Fix this error: read the exact message and stack, name the cause in one line, apply the smallest safe fix, then rerun and paste the real output, because a claim of success without output is not evidence. Do not suppress the warning, change nothing unrelated, and stop once it passes.

### 5. Build Clean

Get this project building and running clean: run the build, read the errors in order, and fix them one at a time, because fixing the third error first usually invents work. Never silence a warning to make it pass. Paste the successful command output, change nothing else, and stop.

### 6. Migration Plan

Write this migration with its rollback in the same change: forward steps, reverse steps, backfill, and safety on existing rows, because a migration you cannot reverse is a decision you cannot undo. Run it dry and paste the output. Do not execute against real data, change nothing else, and stop for my approval.

### 7. Replace Mocks

Replace every mock on this path with the real call, because a step validated on mocked data is a step nobody validated. Remove only what is genuinely mocked, list each one and what now runs instead, exercise the real path, and paste the output. If a credential is missing, say so and stop rather than re-mocking.

### 8. Integrate Api

Integrate this API from its current published docs, not from memory, because the version you remember is usually the one with the vulnerability: typed client, auth, timeouts, retries with backoff, and error mapping. Prove one real call and paste the response. Pin the version, leave unrelated code untouched, and stop.

### 9. Resolve Conflicts

Resolve these conflicts by working out what each side was trying to do, because deleting a hunk to make the merge pass silently discards someone's decision. Keep both behaviors where both are required, change nothing unrelated to the conflict, run the tests, paste the output, and stop before pushing.

## Debug & Trace

![Code Ring / Debug & Trace](previews/code-ring-debug-trace.svg)

### 1. Reproduce Bug

Reproduce this bug end to end, the way a user actually hits it, before you change a single line, because a fix for a bug you never reproduced is a guess with a commit hash. Script the repro if you can, paste the output, report observed versus expected, change nothing else, and stop before editing.

### 2. Read Stack

Read this stack trace precisely: which frame actually failed, what the frames around it were doing, and the likely causes ranked against each other, because the top frame is usually the victim and not the culprit. Name the first thing to check, change nothing else, and stop there.

### 3. Instrument Run

Add minimal targeted logging around the suspected path, run the failing scenario, and read the real output before forming a theory, because a diagnosis without instrumentation is just the most plausible story. Report the values you saw, remove the temporary logging, and stop before fixing.

### 4. Find Bad Commit

Find the commit that introduced this regression using bisect or history, with a fast repro check at each step, because narrowing to one commit turns a hunt into a diff. Report the commit and explain exactly what it broke. Do not fix it yet, change nothing else, and stop.

### 5. Compare Runtime

Inspect the real runtime state at the failure point, variable values, nulls, types, and collection sizes, then paste the values you actually saw and report where reality and our assumptions disagree, because bugs live in that gap. Do not edit anything, touch nothing else, and stop once the mismatch is named.

### 6. Hunt Race

Hunt the race here: shared state, async ordering, awaited versus fire and forget, and locking, because an intermittent failure is an ordering assumption nobody wrote down. Demonstrate the interleaving that fails and paste the evidence. Propose the safest fix in scope, then stop.

### 7. Measure Leak

Find the leak: trace allocations, subscriptions, listeners, timers, and handles created and never released across this repository, because a leak you cannot measure is a leak you cannot prove you fixed. Show the growth with numbers, fix only what you proved leaks, and stop.

### 8. Fix Flaky Test

Kill this flaky test at its root cause, timing, ordering, shared state, or network, because adding a sleep converts a visible flake into an invisible one. Run it repeatedly and report the pass rate over those runs as evidence. Change nothing unrelated, and stop once it is stable.

### 9. Environment Diff

Explain why this works in one environment and fails in another: compare versions, configuration, environment variables, paths, and data, because the decisive difference is always something we assumed was identical. Report the evidence, change nothing else, and stop once you can name it.

## Context & Agent Ops

![Code Ring / Context & Agent Ops](previews/code-ring-context-agent-ops.svg)

### 1. Orient Session

Read the rules file, the plan, the project structure, and the recent git log, then report the files you read, what you understand, and what you believe the next task is, because you have no prior context and I would rather correct your understanding than your diff. Change nothing else, and wait for my confirmation before you touch anything.

### 2. Save State

Write the current state to a file I can hand to a fresh session: what is done, what is in progress, the decisions and their reasons, open questions, and the exact next step, because I am about to clear this window and only the file survives. Report the path, change nothing else, and stop.

### 3. Research Review

Research this task and return findings with source paths. If independent research agents are available and their use is authorized, give them bounded read-only questions and reconcile disagreements. Otherwise do the research yourself and disclose the lack of an independent reviewer. Do not modify files or start implementation.

### 4. Isolate Work

Create a git worktree for this stream so it cannot collide with my other running agents, reinstall the project dependencies inside it, and confirm which worktree and branch you are in, because two agents in one directory overwrite each other. Save it as a reusable command, do not touch my other worktrees, and stop.

### 5. Reuse Workflow

Turn this procedure into a reusable command or skill now that we have done it more than twice: the trigger, the exact steps, and the script that does the real work. Keep it out of the always-on rules file, because this knowledge is only needed sometimes. Report the path, change nothing else, and stop.

### 6. Trim Rules

Audit the rules file line by line, because every line costs tokens on every single request. Move anything conditionally useful into an on-demand reference or a skill, keep only what is always true, and report the before and after line count. Delete nothing I have not approved, and stop.

### 7. Improve Guidance

Do not change any code. Given the mistake we just hit, tell me what to add to the rules, the spec, or the reference files so this whole class of mistake cannot recur, because fixing the instance leaves the cause in place. Check whether an existing rule already covers it, name the exact file for each change, change nothing else, and stop for my approval.

### 8. Map Repo

Map this repository for the work ahead: entry points, the modules involved, the data flow, where the tests live, and every file this will touch. Cite a path and symbol for each claim and check every path exists, because an uncited map is a guess. End with the minimal execution plan, edit nothing, and stop.

### 9. Session Summary

Summarize this session into a file: files touched, behavior changed, decisions and why, tests added, and what is still open, because tomorrow the question is not what this project does but what I was in the middle of. Report the path, add nothing else, and stop.

## Git & PR

![Code Ring / Git & PR](previews/code-ring-git-pr.svg)

### 1. Write Pr

Write the PR body for every change on this branch: original intent, what changed, how it was tested, links to the evidence, and the risk level, because a reviewer who has to reconstruct intent reviews the diff and not the decision. Cite real paths, add nothing else, and do not push.

### 2. Review Diff

Review this branch as a hostile reviewer whose only job is to find defects, in a fresh mindset, because the author of a change is the worst person to judge it. Rank findings by severity with file and line evidence, flag only what you can confirm, and do not edit anything yet.

### 3. Explain Diff

Walk me through all the changes on this branch file by file: what each hunk does, why it is needed, and which hunks deserve a second pair of eyes, because the risky hunk is rarely the biggest one. Show the diffstat output first, flag only what is real, and do not edit anything.

### 4. Split Commits

Split this work into commits a human can actually review: one logical change each, conventional messages, unrelated edits excluded, because a single blob commit is a review nobody performs. Report the planned sequence and run the checks. Do not push or merge without my approval.

### 5. Answer Review

Answer every open review comment: agree and fix, or disagree with a technical reason, because an unanswered comment reads as ignored. Keep replies short and specific, run the checks after each fix, and report the output. Leave unrelated code untouched, and do not merge.

### 6. Write Changelog

Write the changelog entry for all the changes on this branch, in this project's existing style: user-visible impact first, breaking changes flagged, migration notes where they apply, because a changelog written for maintainers helps nobody. Check each claim against the code, add nothing else, then stop.

### 7. Rebase Plan

Inspect the working tree, current branch, configured remote and locally available default-branch reference. State if the reference may be stale. Identify likely conflicts and unrelated commits, then propose the exact rebase steps, recovery path and validation commands. Preserve uncommitted work. Do not fetch, rebase, resolve conflicts, rewrite history, force-push or merge until I approve the plan.

### 8. Issue Report

Write a minimal, complete issue report for this bug: title, environment, steps, expected versus actual, the smallest reproduction, and the suspected area, because an issue nobody can reproduce is a note to self. Confirm the repro by running it, paste the output, change nothing else, and stop.

### 9. Release Notes

Write release notes for humans from all the changes since the last release: what users gain, what behavior moved, upgrade steps, and known issues, because internal jargon in release notes is a support ticket waiting to happen. Check every claim against the shipped code, add nothing else, then stop.

## Ship & Harden

![Code Ring / Ship & Harden](previews/code-ring-ship-harden.svg)

### 1. Release Review

Take this repository to production ready: close the open issues, run tests, lint, and build, refresh the docs and changelog, and produce the exact safe ship commands, because a release assembled by hand is a release with a step missing. Paste the output, leave unrelated behavior untouched, and do not push or deploy without my approval.

### 2. Go / No-Go

Run a release readiness check across versioning, migrations, compatibility, secrets, configuration, packaging, tests, CI, rollback, observability, and docs, because a go decision without a rollback plan is a hope. Report a go or no-go with the blocking items named, change nothing else, and stop.

### 3. Prove Journey

Prove the user journey end to end through the real entry point, real persistence, and the visible outcome, because a passing unit test is not evidence that the product works. Capture a screenshot, recording, or log as proof, list every boundary you could not exercise, change nothing else, and stop before fixing.

### 4. Test Coverage

Design and run a repository-wide test blitz across unit, integration, regression, error-path, and smoke coverage, because a suite that only covers the new code cannot catch what the new code broke. Before you fix anything, report the failure list ordered by blast radius; then fix only what is in scope and show the passing output.

### 5. Hunt Bugs

Hunt for the bugs no test covers across this repository: invariants, error paths, state transitions, concurrency, resource cleanup, and boundary inputs, because the tests encode what we already thought of. Reproduce and rank each issue with evidence, fix only what is in scope, and stop.

### 6. Audit Repo

Audit this repository for authentication, authorization, input validation, injection, secrets, privacy, dependency, and error-leak risks, because the surface you did not audit is the one that ships. Rank concrete findings with paths, run the checks you can and paste the output, propose a fix for each, change nothing unrelated, and do not change auth or secrets without my approval.

### 7. Refactor Behavior

Refactor for clarity and maintainability without changing behavior: lock the current behavior with a test first, then simplify structure, names, and duplication one module at a time, because a refactor without a lock is a rewrite with optimism. Prove parity by running both, and stop.

### 8. Profile Performance

Profile before you optimize anything, because the bottleneck is almost never where it feels like it is. Quantify the cost, propose the lowest-risk improvement, apply only what you measured, and report the before and after numbers. Do not make speculative changes, and stop once it is measured.

### 9. Assess Architecture

Assess this architecture against the goal and the constraints: map dependencies and data flow, compare the alternatives, and propose the smallest sustainable evolution with migration and rollback steps, because a rewrite proposed without a payoff is ambition. Record it as an ADR, check every path you cite, change no code, and stop.

## Explain & Learn

![Code Ring / Explain & Learn](previews/code-ring-explain-learn.svg)

### 1. Explain Code

Explain this code the way a patient senior would: what it does, why it is written this way, the patterns in play, and the two things most worth understanding deeply, because reading code you do not understand is how architectural debt lands. Cite the lines you mean, check them as you go, and edit nothing.

### 2. Explain Error

Explain this error in plain language: what the message actually means, the usual causes ranked, how to confirm which one applies here, and the canonical fix, because the message is written for the compiler author and not for me. Name the check that settles it, edit nothing else, and stop.

### 3. Teach Pattern

Teach me the pattern behind this code: the problem it solves, how this implementation applies it, when to reach for it, and when it is overkill, because a pattern applied without its problem is just ceremony. Show a short example you can run, edit nothing, and say plainly where you are unsure.

### 4. Compare Libraries

Compare the candidate libraries for our specific case on maturity, API fit, performance, dependency weight, and maintenance risk, because the popular choice and the right choice are different questions. Check the current published versions, recommend one as a short ranked list, install nothing, and stop.

### 5. Show Idiomatic

Show me the idiomatic version of this code for this language and framework, as an experienced maintainer would write it, and explain each meaningful difference, because unidiomatic code costs a reader more than it saved the writer. Run it to confirm parity, apply nothing yet, edit nothing else, and stop.

### 6. Useful Comments

Add comments only where they carry intent, invariants, or a non-obvious decision, because a comment that restates the code is a second thing that can go stale. Never narrate what the line already says. Report the comments you added and why, change nothing else, and stop.

### 7. Explain Framework

Explain what the framework is doing invisibly here: the lifecycle, injection, reactivity, or code generation involved, and trace one real request or render through it step by step, because magic you cannot trace is magic you cannot debug. Cite the framework source, check it as you go, and edit nothing.

### 8. Write Report

Write a deep report to a markdown file rather than to this chat, because a long answer in the window is an answer I lose at the next clear: the question, what you checked, the evidence with paths, the conclusion, and what remains uncertain. Report the file path, edit nothing else, and stop.

### 9. Decision Record

Record this decision as an ADR in the repo: the context, the options considered, the decision, the consequences, and what would cause us to revisit it, because a decision nobody wrote down gets relitigated every quarter. Check every path you cite, add nothing else, and stop.

## Env & Tooling

![Code Ring / Env & Tooling](previews/code-ring-env-tooling.svg)

### 1. Fix Ci

Fix this CI run: read the actual log, find the first real failure rather than the downstream noise, reproduce it locally, then fix it, because chasing the last error in the log fixes a symptom. Paste the passing run output, change nothing unrelated, and stop before merging.

### 2. Pin Versions

Pin every dependency to an exact current version, checking what is actually published today rather than what you remember, because models reach for older packages and older packages carry known vulnerabilities. Report the pinned list and run the install. Do not change any major version here, touch nothing else, and stop.

### 3. Upgrade Deps

Upgrade the outdated dependencies in risk order, reading the breaking-change notes first and running the tests between every step, because a batch upgrade that fails tells you nothing about which package did it. Upgrade one package at a time, paste the output at each step, and stop at the first real break.

### 4. Security Scans

Turn on dependency and code scanning for this repository before the next merge, because a vulnerability found by a bot is cheaper than one found by a user. Report the exact configuration you added and run it once to confirm it reports. Do not change application code, touch nothing else, and stop.

### 5. Verify Harness

Build a harness that lets you exercise this product headlessly and check your own work, because an agent that cannot run the thing it changed is guessing. Make it one repeatable command, run it, and paste the output. Leave the existing tests untouched, do not weaken any assertion to make it pass, then stop.

### 6. Enforce Style

Consolidate linting and formatting into tools that run in CI, generating configuration that matches this codebase's dominant style, because a style rule written in prose is a rule nobody enforces. Report what you suppressed and why, run the full check, leave unrelated files untouched, and do not change any logic.

### 7. Faster Checks

Measure the current build, test, and reload times, find the dominant cost, and apply only the highest-impact safe improvement, because a feedback loop slower than my attention span is the real bottleneck. Report the before and after numbers, change nothing unrelated, and stop there.

### 8. Dev Scripts

Create the developer scripts this repo is missing, run, test, lint, format, and clean, and wire them into the task configuration, because a command nobody can find gets reinvented wrong. Run each one, paste the output, document them in the README, add nothing else, and stop.

### 9. Fresh Setup

Write the exact setup steps for this project on a fresh Windows machine: prerequisites, install commands, environment variables, first run, and how to verify each step worked, because setup instructions nobody tested are fiction. Check each command against the repo, touch nothing else, and stop.

## Correct & Recover

![Code Ring / Correct & Recover](previews/code-ring-correct-recover.svg)

### 1. Find Missed Work

List every place in this repository that should have changed alongside what you just edited but did not: callers, types, tests, config, docs, sibling modules, and error paths. Cite a path and symbol for each, because an uncited miss is only a guess. Report the list ranked by blast radius. Do not fix anything, change nothing else, and stop.

### 2. Checkpoint

Before editing, inspect the worktree and identify existing work. Propose a recoverable checkpoint for this task only. Do not stage unrelated files, secrets, or personal data. Create a branch or local checkpoint only within my authorization, and report its name and commit if created. Ask before pushing anywhere. Preserve all existing work.

### 3. Safe Undo

Prepare an undo of only the changes you made in this run. First show the exact diff and distinguish my pre-existing work or other agents' changes. Explain anything that cannot be recovered and ask before deleting or discarding data. Do not use a blanket reset or touch unrelated work. After approval, apply the scoped undo, verify it and stop.

### 4. List Callsites

Before changing this signature or shape, enumerate every callsite, import, test, mock, and serialized copy that depends on it, using exact symbol search rather than a semantic guess, because approximate retrieval misses the ones that matter. Paste the list with paths and line numbers, change nothing else, then stop.

### 5. Break Loop

Stop retrying, because you have failed the same way more than twice. Write to a file what you attempted, the actual error output each time, and what you now believe is wrong, because the next attempt should start from that evidence in a clean window and not from this one. Do not edit, and change nothing else.

### 6. Show Output

Paste the proof of what you just claimed: the actual terminal output, screenshot, or file diff, because I do not accept a summary as evidence. If you did not run it, say so plainly before you continue. Name the exact command and the directory you ran it in, and add nothing else.

### 7. Worktree Plan

Plan up to four independent work streams. Identify shared files, dependencies and likely collisions; propose a separate branch and worktree path for each stream, plus validation and merge order. If the work cannot be split safely, recommend sequential execution. Do not create branches or worktrees, launch agents, edit files or merge anything until I approve the plan.

### 8. Verify Finding

Take the finding you just reported and try to disprove it three separate ways: reproduce it, read the code path that contradicts it, and check whether a test already covers it. Report which attempts failed to refute it, because a claim I cannot falsify is not worth acting on. Do not edit anything yet, change nothing else, and stop.

### 9. State Uncertainty

Before you continue, list what you are actually unsure about here: the assumptions you never validated, the files you never opened, and the claims you only inferred. If the data is insufficient, say so instead of guessing, because a confident wrong answer costs me hours. Report the list and change nothing else.

## More workflows

![Code Ring / More workflows](previews/code-ring-home-more.svg)

### 1. Env & Tooling

Open [Env & Tooling](previews/code-ring-env-tooling.svg).

### 2. Correct & Recover

Open [Correct & Recover](previews/code-ring-correct-recover.svg).
