# Kill Gate

## Objective
Evaluate whether PromoLeak passed the first 30-day validation gate or should be killed, paused, or redesigned.

## Prerequisites
- 30-day outreach period is complete, or enough negative evidence exists to decide early.
- Outreach, call, pilot, and audit results are tracked.
- The evaluator is willing to kill the idea if hard criteria fail.

## Inputs
- Outreach tracker.
- Discovery-call notes.
- Document-access outcomes.
- Paid audit or pilot outcomes.
- First audit findings if any.

## Instructions
1. Count qualified brands contacted.
2. Count serious discovery calls.
3. Count paid audits or NDA-backed document-access pilots.
4. Check whether first document audits found at least 20k PLN per brand in recoverable or preventable leakage.
5. Identify the main bottleneck: demand, document access, leakage size, recoverability, buyer trust, or execution.
6. Decide: continue, narrow, pivot, or kill.
7. Do not count praise or "interesting idea" responses as validation.

## Subagents
- Use one subagent to independently challenge the decision.
- Use one subagent to inspect whether the evidence supports continuation.

## Output
Return a decision memo with:
- contacted count
- serious-call count
- document-pilot count
- paid-conversion count
- leakage evidence
- pass/fail against kill criteria
- decision
- next 14-day action plan if continuing
