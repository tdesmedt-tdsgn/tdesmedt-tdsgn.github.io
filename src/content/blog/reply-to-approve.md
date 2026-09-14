---
title: "A human approval gate that isn't a dashboard"
description: "The cheapest way to keep a human in the loop on an agent pipeline is a reply-matching gate on a channel people already check. The hard part is what happens when the reply doesn't parse."
pubDate: 2026-09-14
tags: [ai, agents, engineering]
demo: https://github.com/tdesmedt-tdsgn/labs/tree/main/reply-to-approve
businessNote: "You do not need a new approval tool to keep a human in the loop on automated work. You need one auditable checkpoint, in a channel your people already read, that refuses to proceed unless someone says yes in a form a machine can recognise. Ask whoever owns your agent work two questions: what exactly counts as approval, and what happens when the answer is ambiguous. If the second question has no answer, the checkpoint is decorative, because a system that interprets hesitation as consent is not gated. Built this way it is days of work rather than a quarter, and the audit trail is a side effect rather than a feature you pay for."
---

The pipeline that produced this post cannot publish anything until I reply to
an email. There is no review dashboard, no queue, no approvals inbox. It opens
a GitHub issue with a handful of pitches, emails me, and then blocks until I
answer with something it recognises. The gate is two regular expressions and a
polling loop. The design work was almost entirely in what happens when my
reply does not parse, which turns out to be most of the time.

## Why the checkpoint is the bottleneck

Agent autonomy is the live question in most organisations this year, and the
blocker is rarely model quality. It is that nobody wants to be the person who
let an automated system ship something unreviewed. So the work stalls in
pilot, or it gets scoped into a review tool: a queue, an auth model,
notifications, an audit trail, a sprint or three of front-end work.

That tool then has a second problem. It is somewhere people have to remember
to go. A checkpoint nobody visits is worse than no checkpoint, because it
launders the decision: the record says approved, and what actually happened is
that a queue grew until someone cleared it.

The channel people do check is their mail. If the approval lives there, the
checkpoint costs almost nothing to build and nothing at all to adopt. GitHub
issues are a convenient backend for this because replying to the notification
email posts a comment, so the audit trail assembles itself: author, timestamp,
exact words, permanently attached to the thing being approved.

## The grammar, and the word "unclear"

The gate reads comments and maps each one onto a decision. `go 3` approves
pitch three. Trailing text is kept as steering, so `go 2 but shorter, focus on
cost` carries the instruction along. `skip` rolls the batch over. Anything
else is unclear.

```python
APPROVE_RE = re.compile(r"^\s*go\s+(\d+)\s*(.*)$", re.IGNORECASE)
SKIP_RE = re.compile(r"^\s*skip\s*$", re.IGNORECASE)

def parse_reply(body: str) -> Decision:
    for line in _own_words(body):
        m = APPROVE_RE.match(line)
        if m:
            return Decision("approve", int(m.group(1)), m.group(2).strip())
        if SKIP_RE.match(line):
            return Decision("skip")
    return Decision("unclear")
```

Three outcomes, and the third is the one that earns trust. An agent that
guesses at "these all look interesting" is not gated at all. The rule is that
unclear never proceeds, and the gate says so out loud rather than sitting
silent: it posts one clarification comment, then keeps waiting. If the
deadline passes with nothing recognisable, it exits with a code that means
escalate. There is deliberately no outcome that means probably fine.

`_own_words` exists because replying by email is the whole point, and mail
clients append things. A reply arrives as your sentence, then an attribution
line, then the entire original message quoted with `>` markers, which includes
the instructions telling you to reply `go N`. The gate reads down your own
lines and stops at the first quoted or signed-off line. Without that, the
pitch list quoted back at the bottom of your mail can approve itself.

## Who is allowed to decide

Eligibility is three filters, and each one is a way the gate quietly opens
itself if you leave it out.

```python
allowed = {a.lower() for a in approvers}
return sorted(
    (c for c in comments
     if c.author.lower() in allowed
     and MARKER not in c.body
     and c.created_at > opened_at),
    key=lambda c: c.created_at,
)
```

A stranger commenting `go 1` on a public repository is not an approver. A
decision from a previous round is stale rather than valid, which matters as
soon as a gate restarts. And the marker filter is the one I did not see
coming.

My pipeline posts with my own personal access token, so its comments arrive
under my login. Author filtering therefore does not exclude the pipeline from
itself. That would be harmless, except the clarification comment it posts
contains a worked example, on its own line, so the reader knows what a valid
reply looks like:

    Reply with a choice on its own line, for example:

    go 2

That comment parses perfectly as an approval of pitch two. A gate with only
an author filter would ask for clarification, then read its own request as the
answer. So every comment the pipeline writes carries an HTML marker, and the
gate skips anything carrying it. The end-to-end test reproduces exactly this
trap: the fake API posts under the approver's own login, and the run asserts
the gate still ships nothing.

One more rule, from the same family: among comments that already exist, the
newest decision wins. If a gate restarts and finds `go 2` above a later
`go 5`, the later one is what I currently mean.

## What I measured

`verify.sh` runs 27 tests plus one end-to-end pass where the gate runs as its
own process and polls a real HTTP API over a socket. Two rounds, in the order
that matters. First I reply with something friendly and unparseable: the gate
polls three times over 4.09 seconds, posts exactly one clarification, and
exits 12, having built nothing. Then I reply with the grammar: it finds the
decision on the first poll, 0.09 seconds, exit 0, choice 3, steering intact.
Four API calls across both rounds.

The blocked round is the result I care about. A human did reply, the reply was
perfectly clear to a human, and the pipeline still shipped nothing.

There is also an opt-in live pass against api.github.com, and it is the part
that made me trust the thing. It reads the real issue that commissioned this
post and returns `go 3`, comment 5656544412: the gate read the approval that
caused the gate to be written about. The bot comment in the same thread was
correctly excluded.

The whole gate is 97 non-blank, non-comment lines, including docstrings. The
GitHub adapter is another 50, and the gate logic never imports it, so a Slack
or IMAP source is a drop-in swap.

I got one thing embarrassingly wrong on the way. My first test for the
self-approval trap passed immediately, which should always be suspicious. It
passed because the body I had written said "reply `go N`", and `N` is not a
digit, so the grammar rejected it for reasons that had nothing to do with the
filter I thought I was testing. A test that cannot fail is documentation with
a green tick on it. I rewrote it to use a body that genuinely parses, watched
it fail, and only then added the filter back.

## Honest limits

This is polling, not webhooks, which is right for one gate a week and wrong
for a thousand. It reads a single page of 100 comments. And "ask for
clarification once" holds within one process only, because nothing is
persisted: restart the gate and it nudges again. None of that is hard to fix,
and none of it needed fixing to make the checkpoint real.

The deeper limit is that a gate is a checkpoint, not an authorisation system.
It answers "did a named human say yes, in writing, before this shipped". For
a weekly blog pipeline that is the whole question. For anything touching
money or customer data, it is the first question of several.


A gate that blocks on a matching reply is the smallest thing that turns "the
agent shipped it" into "I approved it, here is where I said so". The code is
in the [demo](https://github.com/tdesmedt-tdsgn/labs/tree/main/reply-to-approve),
including the trap where the pipeline nearly approved itself.

Working on something similar? → tom@tdsgn.be
