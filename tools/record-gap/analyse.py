"""Record-gap demo, step 2 -- ask each version of the record the same questions.

Reads case.json, writes gap_report.json.

The questions are not invented. Gard names them: the surveyor could not establish
"running hours, overhaul history and the reasons for those changes", and so could
not tell whether the damage "was part of a wider issue affecting all three
generators or a separate issue affecting only that turbocharger".

So this asks exactly those four things, of each record, mechanically. Nothing here
asserts an answer -- every verdict below is computed by searching the rows, and if
the rows change the verdicts change. That matters, because a demo whose conclusion
is written into the narration proves nothing.

Two rules inherited from tools/phase1 and they apply here:

  Report what the record can and cannot ESTABLISH. Never adjudicate. No monetary
  figures, no policy interpretation, no view on whether an insurer should pay.
  Whether damage falls within a wear-and-tear exclusion is a contested question
  and this tool stops well short of it.

  The negative results are load-bearing. `not_fixed_by_coholding` is not a
  disclaimer, it is a finding, and it is the section to read first if you are
  trying to decide whether any of this is worth building.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "case.json")
OUT = os.path.join(HERE, "gap_report.json")

# The lube oil batch is the common cause. Finding it is finding the answer.
BATCH = re.compile(r"LO-\d{4}-[A-Z]")


def rows_for(records, dg=None, codes=None):
    out = records
    if dg:
        out = [r for r in out if r["dg"] == dg]
    if codes:
        out = [r for r in out if r["job_code"] in codes]
    return out


def q_running_hours(records):
    """Can running-hour history be reconstructed for each generator?

    A single current counter reading is not history. What the surveyor needs is
    hours against events, so that an interval can be checked against the maker's
    recommendation.
    """
    per_dg = {}
    for dg in ("DG1", "DG2", "DG3"):
        pts = sorted({r["done_rh"] for r in rows_for(records, dg=dg)})
        span = (max(pts) - min(pts)) if len(pts) > 1 else 0
        per_dg[dg] = {"datapoints": len(pts), "rh_span_covered": span}
    total = sum(v["datapoints"] for v in per_dg.values())
    return {
        "question": "Can running hours be established against maintenance events?",
        "per_generator": per_dg,
        "status": "answerable" if all(v["datapoints"] >= 3 for v in per_dg.values())
                  else "unanswerable",
        "note": "A live counter gives one number. History needs hours attached to "
                "events." if total < 9 else "",
    }


def q_overhaul_history(records):
    """What turbocharger work was done, on which sets?"""
    work = {}
    for dg in ("DG1", "DG2", "DG3"):
        rs = rows_for(records, dg=dg, codes={"TC-REP", "TC-INS", "TC-DMG"})
        work[dg] = [{"date": r["done_date"], "rh": r["done_rh"],
                     "job": r["job_title"]} for r in rs]
    found = sum(len(v) for v in work.values())
    return {
        "question": "What turbocharger work was carried out, and on which sets?",
        "work": work,
        "status": "answerable" if found >= 4 else "partial",
        "note": "The fact of the two cartridge replacements survives, because the "
                "purchase orders sit in the owner's own accounts rather than in the "
                "manager's PMS." if found < 4 else "",
    }


def q_reasons(records):
    """WHY were the turbochargers on DG2 and DG3 changed?

    This is the one that decides the case, and it is the one that lives in a free
    text remarks field -- the least portable thing in any PMS export.
    """
    reasons = []
    for r in rows_for(records, codes={"TC-REP", "TC-INS", "TC-DMG"}):
        if r.get("remarks", "").strip():
            reasons.append({"dg": r["dg"], "date": r["done_date"],
                            "reason": r["remarks"]})
    return {
        "question": "Why were the turbochargers on DG2 and DG3 changed?",
        "reasons_recorded": reasons,
        "status": "answerable" if len(reasons) >= 3 else "unanswerable",
        "note": "Replacement is visible; cause is not. The remarks field did not "
                "survive." if len(reasons) < 3 else "",
    }


def q_causation(records):
    """One issue across all three sets, or one isolated failure?

    Computed, not asserted: look for a batch reference shared across events on
    more than one generator. If a common token links them, the link is findable.
    If not, it is not.
    """
    hits = {}
    for r in records:
        for m in BATCH.findall(r.get("remarks", "") or ""):
            hits.setdefault(m, set()).add(r["dg"])
    linked = {k: sorted(v) for k, v in hits.items() if len(v) >= 2}
    all_three = any(len(v) == 3 for v in linked.values())
    return {
        "question": "Was the DG1 damage part of a wider issue affecting all three "
                    "generators, or isolated to that turbocharger?",
        "common_references_found": linked,
        "generators_linked": max([len(v) for v in linked.values()], default=0),
        "status": "answerable" if all_three else "unanswerable",
        "finding": ("A single shared cause reference appears against all three "
                    "generators.") if all_three else
                   ("No shared reference links any two generators. On this record "
                    "the three events are three unrelated events."),
    }


def gap_census(truth, received):
    """How much is missing, and can you tell?

    This is the actual difference, and it is not 'we have the records' versus 'we
    do not'. It is 'we cannot tell what we are missing' versus 'we can count it'.

    Under co-holding each author writes a sequential chain and the owner holds it
    as it is written, so a missing entry shows up as a hole in a sequence. A PMS
    export carries no such structure: rows arrive as a pile, and an absent row is
    indistinguishable from a job that was never done.
    """
    by_author = {}
    for r in truth:
        by_author.setdefault(r["manager"], []).append(r["seq"])
    got = {r["seq"] for r in received}

    per_author = {}
    for mgr, seqs in by_author.items():
        missing = [s for s in seqs if s not in got]
        per_author[mgr] = {
            "entries_written": len(seqs),
            "entries_held": len(seqs) - len(missing),
            "entries_missing": len(missing),
        }
    return per_author


def assess(records, truth, label, countable):
    return {
        "record": label,
        "entries_available": len(records),
        "gap_is_countable": countable,
        "gap_census": gap_census(truth, records) if countable else None,
        "questions": [q_running_hours(records), q_overhaul_history(records),
                      q_reasons(records), q_causation(records)],
    }


def main():
    with open(CASE, encoding="utf-8") as f:
        case = json.load(f)
    rec = case["records"]
    truth = rec["truth"]

    # The handover pack carries no per-author sequence, so the gap cannot be counted
    # from it -- you would need the thing you do not have in order to measure what
    # you do not have. The co-held record carries the sequence by construction.
    handover = assess(rec["handover"], truth, "As received at handover",
                      countable=False)
    coheld = assess(rec["coheld"], truth, "Co-held at write time", countable=True)

    report = {
        "_disclosure": case["_disclosure"],
        "vessel": case["vessel"],
        "incident_date": case["incident_date"],
        "handover_date": case["handover_date"],
        "assessments": [handover, coheld],
        "not_fixed_by_coholding": [
            "It cannot recover a reason that was never written down. If the engineer "
            "logged the cartridge change and not the cause, no arrangement about "
            "custody puts the cause back.",
            "It does not make an entry true. A wrong entry, co-held, is a wrong entry "
            "held by two parties instead of one. This is custody, not verification, "
            "and the difference is the whole reason this is not ValiChord.",
            "It is forward-only. Gard notes the gaps 'may have dated back to previous "
            "ownership or management'. Nothing here reaches back past the day it was "
            "adopted -- the first owner to adopt it still inherits a blank history.",
            "It requires the owner's node to have been online to receive the entry. "
            "A one-ship owner whose machine is off for a month has an availability "
            "problem, and solving that with an always-on peer quietly reintroduces "
            "the operator the design was avoiding.",
            "It does not stop a manager keeping a second, private record. It only "
            "means the entries they DID write cannot later be withdrawn.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("wrote " + OUT)
    for a in report["assessments"]:
        print("\n  " + a["record"] + "  (" + str(a["entries_available"]) + " entries)")
        for q in a["questions"]:
            print("    [%-12s] %s" % (q["status"], q["question"][:64]))
        if a["gap_census"]:
            for mgr, c in sorted(a["gap_census"].items()):
                print("       manager %s: %d written, %d held, %d missing"
                      % (mgr, c["entries_written"], c["entries_held"],
                         c["entries_missing"]))
        else:
            print("       gap cannot be counted -- no sequence to count against")


if __name__ == "__main__":
    main()
