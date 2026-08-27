# 25 — Seven tests before building a verification product

**Seven candidate use cases were investigated properly in this repository. All seven closed.
These are the tests that closed them, in the order they cost least to run.**

Written 27 August 2026. The shipping evidence is the worked example; **the tests are not
about shipping** and should be applied to whatever comes next.

If a candidate fails any one of these, stop. It is cheaper to lose an afternoon than a year.

---

## Run these first — they cost nothing but thought

### Test 1 — Is the dispute about measurement, or about judgement?

> **Could a sensor settle this, in principle, if someone bothered to install one?**

**If yes, walk away.** A sensor will arrive, and it will win. Every time.

| Candidate | What happened |
|---|---|
| Notice of Readiness / laytime | AIS settled it. Marcura and Veson sell the reconciliation |
| Bunker quantity | Mass flow meters settled it. Singapore mandated them in 2017, Rotterdam and Antwerp-Bruges from 2026 |
| Container damage at interchange | Automated gate cameras are settling it now |

Cryptography arrives second in a measurement fight and loses. **It is only worth anything
where two competent people, looking at the same thing, legitimately disagree** — because no
instrument can arbitrate that.

### Test 2 — Who buys it, and who does it constrain?

> **Is the party who would be verified the same party who controls the purchase?**

**If yes, it will not be adopted on merit**, however good it is.

This was the strongest finding in the whole scan. In three of four areas examined in
[`docs/22`](22-why-shipping-resists-this.md), the verification system would have to be bought
by the party it constrains — the owner controls the sensors in a performance dispute, the
terminal owns the gate cameras that might convict it, each surveyor is paid by the side they
advance.

**The sharpest single piece of evidence anywhere in this work** is BIMCO's Energy Efficiency
Data Sharing Clause 2025, sub-clause (k): charterers *"expressly waive any right to use the
Data as a basis for or in support of a claim against the Owners regarding… warranties as to
speed and consumption."*

Better evidence already exists. **The party holding it has contracted it out of the dispute.**

**The one exception is instructive.** Bunker meters *were* forced on the measured party — by
Singapore making them a condition of the bunker licence, not by anyone buying one. If a
candidate fails this test, the only route that has ever worked is **a gatekeeper mandating
it**: a port authority, a regulator, a class society, an insurance pooling agreement. That is
a multi-year play, not a sale.

---

## Then these — an afternoon of desk research each

### Test 3 — Does anyone already sell this?

> **Spend one hour searching before you write a line.**

Obvious, universally skipped, and the reason four phases of engineering in this repository
were spent on a capability Marcura had been shipping for years — an AI pipeline over 700,000
Statements of Facts, reconciled against AIS, integrated with Veson.

Nobody asked until the fifth document. Ask first.

### Test 4 — Does a trusted neutral already exist?

> **When these two parties disagree today, who do they both accept?**

Industries solve trust long before technologists arrive. Look for it in four places:

- **Commercial** — SGS and Control Union sell independence as a brand; Marcura and OceanScore sell reconciliation
- **Statutory** — FuelEU has an accredited verifier who confirms every ship's balance, and an EU registry that records it
- **Contractual** — BIMCO clauses appointing a mutually-agreed expert whose findings bind
- **Social** — the joint survey, where all parties' surveyors attend together

**If any of these exists, trust-minimisation is solving a problem that has already been
solved** — socially, legally, or commercially. That is why every shipping candidate closed.

### Test 5 — Does the mechanism already exist, unused?

> **If the answer is "we should pre-agree a neutral expert" — check whether someone already
> wrote that clause.**

Speed and consumption disputes have no *product* offering neutral pre-committed
adjudication. But London Arbitration 9/23 turned on wording already in use: *"a mutually
agreed weather routing company to be appointed… whose findings will be final and binding."*
BIMCO has published such a clause since 2006.

The industry knows how to write it and largely does not use it.

**When a mechanism exists and is not adopted, the missing thing is not a tool.** Building one
means fighting a problem that is not technical, and losing.

---

## And these — you cannot answer them from a desk

### Test 6 — Would this destroy something that already works?

> **What do practitioners actually do today, and why?**

The marine cargo survey case was this repository's fallback position for four documents. It
was retracted the day someone finally checked practice.

Established practice is the **joint survey**: surveyors for all interests attend together,
explicitly *without prejudice*, and are *meant* to converge on quantum and cause at the scene
so litigation is avoided. Failing to invite the other side can prejudice recovery.

**Blinding them would deliberately destroy the convergence the industry relies on to settle
cheaply.** The anchoring-contamination argument may still be true — but proving it against
entrenched practice that everyone believes works is a research programme, not a product.

Ask three practitioners before you believe your own model of their work.

### Test 7 — Is the false record a symptom of an impossible rule?

> **If people are falsifying a record, ask why — and ask who suffers when they cannot.**

This is the one most likely to be built by someone who did not check, **because it looks
like helping.**

Seafarer hours of rest passed every test above. Real problem, detainable deficiency, fatigue
that kills, no vendor serving the affected party, unilateral adoption, and a record that
genuinely should not live on the employer's system.

Then *"A culture of adjustment"* — World Maritime University, funded by the ITF Seafarers'
Trust — named the mechanism: the regulations are so difficult to comply with that
*"seafarers and inspectors alike… collude in an adjustment to suit the rules rather than
reflect the realities on board."*

**Everyone adjusts, including the inspector**, because the rules cannot be met at current
manning levels.

So an unalterable record would be **a weapon pointed at the seafarer**. An honest log does not
create rest — it creates a detention, and the crew wear it. The person the tool is meant to
protect would refuse to use it, and would be right.

**The falsification is a symptom. The disease was manning levels and regulatory design, and
no amount of evidence integrity touches either.**

This is the only one of the seven that failed on ethics rather than economics.

---

## What survived, because seven tests alone is only demolition

A red-team pass without a blue-team pass produces the belief that nothing is viable, which is
exactly as wrong as believing everything is. Five things came out of this work and all five
are portable.

**1. Validation can verify computation, not merely witness commitment.** FuelEU was the first
candidate where the disputed quantity was arithmetic over committed inputs, so peers could
enforce that a figure was *correct* rather than merely recording that somebody asserted it.
Everywhere else the honest answer was "we can prove you committed to this, not that it is
true." That distinction is where Holochain's validation model is genuinely strong, and it
holds in any domain.

**2. Anchoring-prevention works unilaterally.** One party sealing their position *before*
exposure captures the entire benefit with nobody else participating. **This dissolves the
twelve-counterparty adoption wall that killed TradeLens and Holo Sail**, and it took five use
cases to notice. It is the single most valuable thing found here.

**3. Put the network boundary where the obligation lives.** [`docs/15`](15-dna-architecture.md)
cloned per voyage and destroyed the accumulating history the deterrent depends on. FuelEU
should clone per *vessel*, because the compliance balance attaches to the hull and survives
every change of charterer and manager. **Find where the liability sits, and put the boundary
there** — not where the transaction is.

**4. Countersigning fits handovers, and only handovers.** Where two parties hold opposite
incentives about one number at one moment, atomic bilateral commit is the primitive nothing
else provides. Everywhere else it is overhead.

**5. Offline-first requires no argument about trust.** A source chain signs offline and
gossips on reconnect with its sequence intact. For anything recorded away from connectivity
that is a plain advantage over any hosted platform, and it needs no cryptographic claim to
sell it.

---

## How to use this

Run tests 1 and 2 in ten minutes. Most candidates die there, free.

Run 3, 4 and 5 in an afternoon of searching. Most survivors die there.

Only then spend a week finding three practitioners for 6 and 7 — and go in expecting to be
told you are wrong, because that is the cheapest outcome available.

**Build nothing until all seven pass.**

Seven candidates were run through this in shipping. None passed. The evidence is in
[`docs/20`](20-is-this-already-solved.md), [`docs/22`](22-why-shipping-resists-this.md),
[`docs/23`](23-draft-survey.md) and [`docs/24`](24-fueleu-architecture.md), and the working
demonstrator that came out of the first one is in `tools/`.

That is not a wasted year. It is seven tests, five portable findings, and a public record of
how the work was done.
