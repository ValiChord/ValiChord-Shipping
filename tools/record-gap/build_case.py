"""Record-gap demo, step 1 -- build the vessel's maintenance record.

Reconstructs the SHAPE of the case Gard published on 21 July 2026: a turbocharger
fails on one of three diesel generators, the other two had recent turbocharger
changes, and the records needed to tell whether that is one problem or three are
missing or incomplete.

    Gard, "The risk of taking over a vessel without its history", 21 July 2026.
    Svend Leo Larsen (Senior Claims Adviser), Kristin Urdahl (Loss Prevention
    Specialist).

NOTHING HERE IS A REAL VESSEL OR A REAL CLAIM. Gard published no data, no vessel,
no dates and no running hours. Every row below is invented to the shape of a PMS
export. The vessel does not exist and its IMO number is deliberately invalid. See
README.md. Do not remove the `_disclosure` block from the output.

Three records are written, all from one ground truth:

  truth     what was actually done to the machinery, and why
  handover  what the incoming manager actually received -- the failure mode Gard
            and IUMI describe. Entries written by the outgoing manager are simply
            gone, and nothing indicates how many are missing
  coheld    the same history, had every entry been copied to the owner at the
            moment it was written rather than requested at handover

`coheld` is not a better-behaved manager. It is the same manager, writing the same
entries, under an arrangement where writing publishes. That distinction is the
whole point and the README says so at greater length.
"""
import json
import os
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "case.json")

# --- the vessel -------------------------------------------------------------
# IMO 0000000 is not a valid IMO number. It cannot collide with a real ship.
VESSEL = {
    "name": "M/V NORTHERN CADENCE",
    "imo": "0000000",
    "imo_note": "not a valid IMO number -- this vessel is invented",
    "type": "Bulk carrier",
    "built": 2011,
}

MANAGERS = [
    {"id": "A", "name": "Alpha Ship Management",
     "from": "2023-02-01", "to": "2025-05-15"},
    {"id": "B", "name": "Bravo Marine Services",
     "from": "2025-05-15", "to": "2026-12-31"},
]
HANDOVER = datetime(2025, 5, 15)
INCIDENT = datetime(2026, 6, 18)
START = datetime(2023, 2, 1)

# Three diesel generators. DG1 is the standby set and runs least -- which is why
# it is the last of the three to fail, not the first. That asymmetry is what makes
# the causation question hard, and it is the reason the demo has three DGs.
DGS = {
    "DG1": {"comp": "6XX.001", "rh_start": 21450, "rh_per_year": 1800,
            "role": "standby"},
    "DG2": {"comp": "6XX.002", "rh_start": 38900, "rh_per_year": 4200,
            "role": "main duty"},
    "DG3": {"comp": "6XX.003", "rh_start": 37200, "rh_per_year": 4000,
            "role": "main duty"},
}

# Turbochargers are components in SFI primary group 6 alongside the engines they
# serve. The lubricating oil system is NOT -- group 7 is "systems for machinery
# main components", which is where fuel and LO systems live. That distinction is
# load-bearing here: the LO system is COMMON to all three engines, and a group 7
# code says so where a group 6 code cannot. See tools/pms-model/.
#
# Digits are placeholders. SFI is licensed from SpecTec and we do not have the
# manual, so these are SFI-SHAPED and deliberately not SFI. See tools/pms-model/README.md.
TC_COMP = {"DG1": "6XX.011", "DG2": "6XX.012", "DG3": "6XX.013"}
LO_COMP = "7XX.001"
LO_NAME = "Lubricating oil system, auxiliary engines (common to DG1/DG2/DG3)"

WASH_INTERVAL_RH = 500      # turbocharger water wash


def rh(dg, when):
    """Running hours for a generator at a date. Linear -- a real PMS reads a counter."""
    yrs = (when - START).days / 365.25
    return int(DGS[dg]["rh_start"] + DGS[dg]["rh_per_year"] * yrs)


def date_at_rh(dg, target):
    """Inverse of rh() -- when did this generator reach these running hours."""
    yrs = (target - DGS[dg]["rh_start"]) / DGS[dg]["rh_per_year"]
    return START + timedelta(days=yrs * 365.25)


def mgr_at(when):
    return "A" if when < HANDOVER else "B"


def entry(seq, when, dg, job_code, job_title, remarks, order=None):
    """One PMS row, in the column shape these exports actually arrive in."""
    mgr = mgr_at(when)
    return {
        "seq": seq,
        "component": TC_COMP[dg] if not job_code.startswith("LO-") else LO_COMP,
        "component_name": (LO_NAME if job_code.startswith("LO-")
                           else "Turbocharger, auxiliary engine " + dg[-1]),
        "dg": dg,
        "job_code": job_code,
        "job_title": job_title,
        "done_date": when.strftime("%Y-%m-%d"),
        "done_rh": rh(dg, when),
        "done_by": "Ch/Eng (" + MANAGERS[0 if mgr == "A" else 1]["name"] + ")",
        "manager": mgr,
        "remarks": remarks,
        "order_no": order,
    }


def build_truth():
    """What actually happened to the machinery, in order."""
    rows = []

    # Routine turbocharger water washing, every 500 running hours, all three sets.
    for dg in DGS:
        n = 1
        while True:
            target = DGS[dg]["rh_start"] + n * WASH_INTERVAL_RH
            when = date_at_rh(dg, target)
            if when > INCIDENT:
                break
            rows.append(("wash", when, dg, "TC-CLN", "Turbocharger water wash",
                         "Routine. No abnormality noted.", None))
            n += 1

    # The common cause. A lube oil delivery in Nov 2024 is later found contaminated;
    # it goes to all three sets off the same service tank. This is the fact that makes
    # the three failures one event rather than three, and it is recorded ONCE, by the
    # outgoing manager, six months before the handover.
    rows.append(("lo", datetime(2024, 11, 3), "DG2", "LO-BNK",
                 "Lube oil bunkered - main LO service tank",
                 "LO batch ref LO-2411-B. Supplied to DG service tank common to "
                 "DG1/DG2/DG3.", "PO-24-8871"))
    rows.append(("lo", datetime(2024, 11, 28), "DG2", "LO-SMP",
                 "Lube oil sample - laboratory result",
                 "Sample against batch LO-2411-B returned HIGH particulate count "
                 "and water ingress. Lab flagged abrasive wear risk to TC bearings. "
                 "Tank not renewed - consumed in service.", "LAB-24-3312"))

    # DG2 fails first: highest running hours, so it reaches the damage threshold first.
    rows.append(("tc", datetime(2025, 1, 9), "DG2", "TC-REP",
                 "Turbocharger cartridge replaced",
                 "Bearing wear found on inspection following high exhaust temp and "
                 "vibration alarm. Debris consistent with LO contamination, batch "
                 "LO-2411-B (ref LAB-24-3312). Cartridge renewed.", "PO-25-0104"))

    # DG3 next, three weeks later, and the engineer explicitly links it to DG2.
    rows.append(("tc", datetime(2025, 2, 2), "DG3", "TC-REP",
                 "Turbocharger cartridge replaced",
                 "Same bearing wear pattern as DG2 (ref PO-25-0104). Attributed to "
                 "LO batch LO-2411-B. Cartridge renewed. DG1 inspected, wear present "
                 "but within limits - monitor.", "PO-25-0119"))

    # The inspection finding on DG1 that would have predicted everything.
    rows.append(("tc", datetime(2025, 2, 2), "DG1", "TC-INS",
                 "Turbocharger inspection - bearing clearance",
                 "Bearing clearance at upper limit. Same wear pattern as DG2/DG3 but "
                 "less advanced - DG1 is standby set and has run far fewer hours on "
                 "batch LO-2411-B. Recommend renewal at next opportunity.", None))

    # --- management changes here. Everything above is Alpha's. -----------------

    # And sixteen months later, DG1 does what the inspection said it would.
    rows.append(("tc", INCIDENT, "DG1", "TC-DMG",
                 "Turbocharger damage - bearing failure",
                 "Turbocharger bearing failure in service. Rotor contact with "
                 "casing. Cause under investigation.", "CLM-26-0618"))

    rows.sort(key=lambda r: (r[1], r[2]))
    return [entry(i + 1, w, dg, jc, jt, rm, o)
            for i, (_, w, dg, jc, jt, rm, o) in enumerate(rows)]


def build_handover(truth):
    """What the incoming manager actually received.

    The failure Gard and IUMI describe, modelled exactly:

      * Everything Alpha wrote is gone. Their PMS was their licensed software and
        the data sat in their tenant; access ended with the agreement.
      * Two things survive, because they are not in the PMS at all -- the purchase
        orders for the two cartridges, which are in the OWNER's accounts. So the
        incoming manager can see THAT the turbochargers on DG2 and DG3 were
        replaced, and cannot see WHY.
      * Running-hour counters read live off the machinery. Current value only,
        no history.

    Note what is absent: any indication of how much is absent. That is the part
    that matters.
    """
    kept = []
    for r in truth:
        if r["manager"] == "B":
            kept.append(dict(r, source="Bravo PMS"))
        elif r["order_no"] and r["order_no"].startswith("PO-25"):
            # Survives via the owner's purchase ledger -- stripped to what a PO shows.
            kept.append(dict(r, remarks="", done_by="",
                             source="Owner purchase ledger"))
    return kept


def build_coheld(truth):
    """The same history, had every entry been copied to the owner when written.

    Not a better manager. The same manager, writing the same entries, where the act
    of writing publishes to the other party. Alpha's entries survive Alpha's
    departure because the owner already held them on the day each one was made.
    """
    return [dict(r, source="Co-held at write time (author: manager "
                           + r["manager"] + ")")
            for r in truth]


def main():
    truth = build_truth()
    case = {
        "_disclosure": {
            "what_this_is": "A synthetic reconstruction of the SHAPE of a published "
                            "case, built to test whether co-holding maintenance "
                            "records at write time would change what a claim can "
                            "establish.",
            "real": "The problem, and that it is unresolved. Gard 21 July 2026; Gard "
                    "Loss Prevention Circular 2010; IUMI position paper 'Loss of ship "
                    "records', 8 September 2015 (with the London Joint Hull Committee, "
                    "petitioning IACS); Cefor 2018 statistics on claims frequency at "
                    "change of ownership.",
            "synthetic": "The vessel, its IMO number, both managers, every date, every "
                         "running hour, every maintenance entry and the lube oil batch. "
                         "Gard published no data. No real vessel, manager, owner or "
                         "insurer is depicted, and no real party did anything described "
                         "here.",
            "not_claimed": "That co-holding would have changed the outcome of Gard's "
                           "case. Nobody outside Gard knows what was in that file.",
        },
        "vessel": VESSEL,
        "managers": MANAGERS,
        "handover_date": HANDOVER.strftime("%Y-%m-%d"),
        "incident_date": INCIDENT.strftime("%Y-%m-%d"),
        "generators": {k: dict(v, rh_at_incident=rh(k, INCIDENT))
                       for k, v in DGS.items()},
        "records": {
            "truth": truth,
            "handover": build_handover(truth),
            "coheld": build_coheld(truth),
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(case, f, indent=2)

    t = len(case["records"]["truth"])
    h = len(case["records"]["handover"])
    c = len(case["records"]["coheld"])
    by_a = sum(1 for r in truth if r["manager"] == "A")
    surviving_a = sum(1 for r in case["records"]["handover"] if r["manager"] == "A")
    print("wrote " + OUT)
    print("  entries actually made        %d" % t)
    print("  received at handover         %d" % h)
    print("  co-held at write time        %d" % c)
    print("  written by outgoing manager  %d  (of which %d survived handover)"
          % (by_a, surviving_a))


if __name__ == "__main__":
    main()
