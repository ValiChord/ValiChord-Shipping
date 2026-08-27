# 28 — Prior art, and what the general case actually tells us

Written 27 August 2026, prompted by an external research pass whose leads were then checked
against primary sources. Read after [`27`](27-holochain-1.0-and-what-to-design-for.md).

## First, a correction

`tools/record-gap/README.md` said nobody is paid to prevent this problem, only to remediate
it. **That was too strong.** Someone sells it.

## CoverSense Vessel Passport — real, and the closest prior art found

`coversense.co.uk/passport`. Verified directly, not taken on report.

> *"The permanent digital identity for your boat — a trusted record of every service, repair
> and inspection that stays with the vessel for life."*
>
> *"A permanent, secure digital record attached to your boat — not to you."*
>
> Entries *"cannot be altered or deleted after verification."*

Entries are created automatically when a marine professional completes a job in CoverSense
Log, plus unverified owner notes. On sale, the owner hands over an NFC tag and the buyer taps
it. Free tier with a £5 tag; Passport+ at £4.99/month.

**The general proposition — make the record stay with the vessel — is therefore not novel,
and we should stop implying it is.**

Three differences that still matter, in descending order of importance:

1. **They solved the double-entry problem, and we should learn from how.** Our own README
   says that if the crew must type into two systems it has no users. CoverSense's answer is
   that **the professional is the one who benefits**: the engineer logs the job to prove
   their own work and protect their own business, and the vessel record is a by-product.
   That is a genuinely good design and it is worth stealing. Our equivalent would be finding
   what the *manager's* own reason to write is, rather than assuming the owner can compel it.

2. **"Permanent" is rented.** The record is hosted by CoverSense, and permanence costs
   £4.99 a month. The NFC tag is a pointer, not the data — if the company goes, the tag
   points at nothing. This is the custody question exactly as `27` frames it, and it is
   unresolved rather than answered.

3. **Recreational, not commercial.** A Hallberg-Rassy with one owner and an engineer is a
   different world from a bulk carrier with an owner, a third-party manager, class and an
   H&M underwriter. Our failure mode — the *manager* leaving and taking the record — does
   not really exist in their market.

**None of this kills the candidate. It does mean the pitch can never be "nobody has thought
of this."** It has to be "the hosted version exists; here is why an owner would want one that
does not depend on a host."

## The general case is real, and it is better evidence than it first appears

The external pass proposed a generalisation: *persistent asset records should follow the
asset, not the organisation that happened to maintain it*. Checked across three sectors, it
holds — and each one was verified independently.

**Aviation has priced it.** Asset values drop **10–20% when full back-to-birth traceability
cannot be confirmed** (KPMG aviation finance report, 2024). A single missing trace or an
unresolved AD signature can delay a lease redelivery by three to six weeks and trigger
seven-figure reserve penalties.

**UK buildings have legislated it.** The Building Safety Act 2022 "golden thread" requires
information kept digitally across a building's whole life, with **full transfer of records on
change of ownership**, tamper resistance, an audit trail, and accessibility to those who need
it. That is close to our requirement list, written as law.

**The EU has mandated it with a date.** Under Battery Regulation 2023/1542, every EV and
industrial battery over 2 kWh on the EU market must carry a digital passport from
**18 February 2027** — and it is explicitly the template for Digital Product Passports across
other categories under ESPR (Regulation (EU) 2024/1781).

## But the conclusion to draw is the opposite of "go bigger"

The tempting reading is that this is a larger market than shipping. It is not the reading the
evidence supports.

**In every adjacent sector where this problem got solved, a mandate solved it — and the
mandate created the buyer.** Aviation: the regulator plus lessor contracts, with the value
quantified at 10–20% of the asset. Buildings: an Act of Parliament after Grenfell. Batteries:
an EU regulation with a hard date.

**Shipping is the outlier precisely because it has no mandate.** IUMI asked IACS for exactly
that in 2015 and got nowhere in eleven years. So the general case does not hand us a bigger
market. **It hands us the diagnosis of why shipping is stuck**, and it is the same finding as
[`25`](25-seven-tests.md) test 2, arrived at from outside: the only route that ever worked
was a gatekeeper mandating it.

Two further cautions before anyone reaches for the bigger market:

- **The mandated sectors are a land rush.** A single search on battery passports returns
  several funded vendors already selling into a deadline that has not yet arrived. Arriving
  late to a regulated gold rush is a worse position than being early to an unregulated gap.
- **The mandated sectors have a quantified case and we assumed shipping did not. Wrong —
  see below.**

## Correction: shipping has priced this, precisely and publicly

An earlier draft of this document said aviation had priced the problem and shipping had not,
on the grounds that Gard's article attaches no number. **That was lazy — the number exists,
it is published by the insurers themselves, and it is very close to our case.**

From Cefor's Nordic Marine Insurance Statistics (NoMIS), the Nordic hull underwriters'
own database, covering claims above USD 10,000:

- **Main engine damage is the most expensive machinery claim category**, at roughly
  **35% of machinery claim costs** and an average well above **USD 500,000** per claim.
- **Lubrication failure is the single most frequent *and* most costly cause of main engine
  damage, averaging USD 926,000 per claim** — because of consequential damage to parts
  such as crankshafts.
- The ranking of causes is **lube oil failure first, incorrect maintenance second**, then
  poor fuel management.
- **Eleven machinery claims above USD 5 million in 2024**, against seven in 2023 and nine in
  2022. Machinery claim cost per vessel was **50% higher in 2024 than in 2015–2021**.

And the trend is going the wrong way, which is the part that makes this sellable. Cefor's
press release of 13 April 2026 is titled *"From a silver tsunami to a claims tsunami?"* and
reports 2025 as **the third consecutive year of elevated claims costs**, with machinery
failure and fires the main drivers, *"seen in the context of an ageing fleet."*

**Read the cause ranking again.** The top two causes of main engine damage — lubrication
failure and incorrect maintenance — are precisely the two things a maintenance record either
establishes or fails to. That is not an adjacent statistic. That is the case.

Note also that [`../tools/record-gap/`](../tools/record-gap/) invented a **lubrication
contamination** scenario purely from the shape of Gard's article, before any of this was
known. It landed on the industry's most expensive and most frequent machinery failure cause
by accident. Keep it.

### What is still unpriced

The **increment attributable to missing records specifically**. Nobody has published what an
incomplete record costs on top of the claim itself. But that question now has a denominator,
which makes it a far better question to ask:

> On a lubrication-failure claim averaging USD 926,000, what does an incomplete maintenance
> record change — in recovery from third parties, in deductible treatment, and in time to
> settle?

That is answerable from claims data, it is flattering to be asked, and the answer either
builds the business case or ends it.

### Two people at one small trade association

Worth noticing: **Cefor holds both halves of this.** Helle Hammer, who chairs the IUMI Policy
Forum that raised the records issue in 2015, is at Cefor. So is **Astrid Seltmann, the
Actuary/Analyst named on the NoMIS releases** — the person who would actually know what
missing records do to a claim's cost and duration. Both are publicly listed as press
contacts.

## What this changes, and what it does not

**Name the general case, do not chase it.** "Cross-organisational asset record custody" is a
useful frame because it makes the shipping pitch stronger, not because it is a market:

> Lubrication failure and incorrect maintenance are the top two causes of main engine
> damage, and a lube oil failure claim averages USD 926,000. Both are things a maintenance
> record either establishes or fails to — and records routinely do not survive a change of
> manager. Aviation prices the same problem at 10–20% of the aircraft's value. UK law now
> requires it for higher-risk buildings, transferring on change of ownership. The EU mandates
> it for batteries from February 2027. Shipping is the one sector that hasn't — IUMI asked
> IACS for it in 2015.

That is a far better opening to a P&I club than anything about Holochain, and every clause in
it is verifiable.

**A category is not a customer**, and renaming the project after one is how a solo founder
loses the thread. The discipline in `25` test 2 still applies.

**The one thing that genuinely generalises is the format.** Signed, hash-chained,
per-author-sequenced asset events are sector-neutral by construction — a turbocharger
overhaul, an engine blade inspection and a fire-door installation are the same shape. So the
general case *validates the format-first plan in `27`* rather than changing it. Build the
format so it does not say "ship" anywhere it does not have to, then use it on ships.

## Why it has not been solved — and why it might be doable now

The format was never the hard part. Signed, hash-chained, per-author statements about a
physical thing already exist several times over — GS1 EPCIS, IETF SCITT, W3C Verifiable
Credentials, in-toto, C2PA, git. See the prior-art section of
[`../spec/asset-record-entry-v0.1.md`](../spec/asset-record-entry-v0.1.md).

So the reason asset records still do not survive their custodians is an incentive and
distribution problem. Six blockers, and each one has to be named before any "why now" can be
tested against it.

| # | Blocker | Why it persists |
|---|---|---|
| 1 | **Nobody owns the gap** | The owner feels it every 3–7 years at handover or sale. The manager never feels it. The PMS vendor is *harmed* by fixing it — portability destroys their moat. The insurer pays but does not buy software for owners. No role's week is ruined often enough to go and buy something |
| 2 | **The pain is already someone's revenue** | A migration-remediation industry exists (BASSnet, SpecTec, Sharecat, Prime Marine). Pain converted into billable hours suppresses demand for prevention |
| 3 | **The adopter loses by adopting** | A two-sided cold start where one side is adversarial |
| 4 | **Deferred, probabilistic value** | Pay now, benefit maybe, years later, only on a claim or a sale. Insurance-shaped, and insurance-shaped things are underbought |
| 5 | **No convener** | Formats in shipping get adopted when BIMCO, IMO, IACS or DCSA convene them. IUMI asked IACS in 2015 and got eleven years of nothing |
| 6 | **Nobody is rewarded for 25-year thinking** | A management agreement runs three years. A superintendent's tenure is shorter. The beneficiary is not in the room |

### Five things that are true in 2026 and were not in 2015

**BIMCO already conceded the principle.** SHIPMAN 2024 Clause 22 gives owners ownership of
vessel data. Clause 21 gives them access *through the manager's own platform*. The
norm-setting body granted the right and specified the wrong mechanism — so the argument is no
longer "owners should have a right to their records", which is what IUMI lost in 2015, but
"you already have this right, here is how you would exercise it."
**The gap between Clause 22 and Clause 21 is the product.** → attacks 5 and 3.

**The insurance route around IACS has reopened.** IUMI's members are underwriters, and an
underwriter does not need IACS to attach a policy condition. They almost certainly went to
class because of collective action: in a soft market, whoever attaches an awkward condition
loses the account. They wanted a universal rule so nobody could undercut them. What has
changed is the market — Cefor reports 2025 as **the third consecutive year of elevated
claims**, machinery cost per vessel 50% above 2015–21. **A hardening market is exactly when
underwriters regain the ability to attach conditions.** → attacks 5 and 4.

**Starlink removed the feasibility constraint.** In 2015 bandwidth was USD 3,000–5,000 per
gigabyte and continuous replication off a ship was impossible; the only available shape was
batch export at handover, which is the thing that fails. **So the absence of this product in
2015 is not evidence anyone judged it uneconomic — it is evidence they could not build it.**
That matters, because "sixteen years and nobody did it" is otherwise the most discouraging
fact in this repository. → removes the precondition, and weakens the strongest argument
against.

**The cost of attempting it collapsed.** In 2015 this was a consortium platform with servers,
governance and a legal entity — that is TradeLens, and it cost Maersk and IBM a great deal
before they shut it. In 2026 the minimum viable version is signed JSON, a peer-to-peer
library, an HTTP gateway and one person. **The problem no longer has to be worth $50m to
justify an attempt; it has to be worth one person's time.** → lowers the bar the demand must
clear.

**Golden Thread and the EU passports normalised the idea.** Weakest of the five: climate, not
a lever. It gives no buyer. It means "records follow the asset" no longer has to be justified
from first principles. → mildly attacks 6. Useful for the pitch, not the economics.

### The scorecard, stated honestly

| Blocker | Status |
|---|---|
| 1 — nobody owns the gap | **Partially improved.** SHIPMAN gives the owner a hook. The pain is still episodic |
| 2 — pain is someone's revenue | **Completely untouched** |
| 3 — the adopter loses by adopting | **Improved, not solved. This is the hard one** |
| 4 — deferred, probabilistic value | **Meaningfully attacked** by the rising loss trend |
| 5 — no convener | **Routed around, not solved.** IACS still has not moved |
| 6 — no reward for long thinking | **Mildly improved** |

Two of six meaningfully attacked, three partially, **one untouched** — plus feasibility and
cost transformed.

That is not a green light. It is a defensible answer to "why has nobody done this" that does
not require anyone to have been stupid. And it locates the whole remaining risk in **blocker
3**.

### What would kill it, decided in advance

Recorded now so that a later session — or a bad week — checks against a fixed test rather
than a moving one.

**Ask three or four people. If all of the following come back empty, stop.**

1. **Nobody can say what a missing record costs them.** If Gard and Cefor cannot attach a
   number or a duration to it against a USD 926,000 average claim, there is no budget line
   and there never will be.
2. **No manager can name a reason they would write into it.** Blocker 3. If the only answer
   is "because the owner makes me", it will not survive a competitive tender.
3. **Owners do not recognise the Clause 22 / Clause 21 gap as a problem they have.** If they
   shrug at it, the sharpest framing available does not land.
4. **An underwriter says they would never attach a condition like this**, even in a hardening
   market. That closes the only convener route left.

If two or more come back positive, it is worth building. **If all four come back empty, this
is candidate eleven and it dies like the other ten** — and that is a good outcome, reached
cheaply.

## The question this all sharpens

The external pass ended on the right question, and it is worth recording verbatim because it
is the one a conversation with Gard should settle:

> **Is there a commercially meaningful gap between "the owner owns the data" and "the owner
> continuously possesses an independently maintained copy of the data"?**

If yes, there is something here. If no, then contractual data-ownership clauses plus an
export function are enough, and CoverSense's hosted model is enough for anyone who wants
more. Note that SHIPMAN 2024 Clause 22 already grants the first half — ownership — and the
problem persisted anyway. That is suggestive, but it is not proof, and it is not answerable
from a desk.
