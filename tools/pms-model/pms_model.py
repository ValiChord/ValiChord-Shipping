"""What is actually inside a ship's planned maintenance system.

Built from public sources so that tools/record-gap/ stops using a schema invented
to fit an article. Every item carries a confidence marker, because the point of
this file is to be *corrected by someone who knows*, and an expert cannot correct
what does not say how sure it is.

    HIGH    stated directly by a primary or near-primary source, cross-checked
    MEDIUM  stated by one credible source, not cross-checked
    LOW     inferred, or sources disagree. Assume wrong until told otherwise

Sources are named inline. Where two sources conflict the conflict is recorded
rather than resolved -- resolving it by picking a favourite is how a plausible
but wrong model gets built.

IMPORTANT LICENCE NOTE. The SFI Group System is not free. An SFI User Licence
Certificate must be purchased from SpecTec, per ship or site. This file therefore
records SFI's *structure*, which is publicly described, and does NOT reproduce
the SFI code tables, which are not. Specific three-digit subgroup values below
are SFI-SHAPED PLACEHOLDERS, not SFI codes. Do not ship them as SFI codes.
"""

# --- SFI Group System --------------------------------------------------------
# HIGH. Released 1972 by the Ship Research Institute of Norway; now sold and
# maintained by SpecTec, who also own AMOS. Widely described as the most used
# classification system in maritime and offshore. 6000+ installations.

SFI_PRIMARY_GROUPS = {
    1: "General",
    2: "Hull systems",
    3: "Cargo equipment",
    4: "Ship equipment",
    5: "Crew and passenger equipment",
    6: "Machinery main components",
    7: "Systems for machinery main components",
    8: "Common systems",
}
# Groups 0 and 9 are left free for users to classify anything SFI does not cover.
# Confidence: HIGH.

SFI_GROUP_NOTES = {
    6: "Primary components in the engine room -- main and auxiliary engines, "
       "propellers, plant, boilers, generators.",
    7: "Systems SERVING the main machinery -- fuel and LUBRICATING OIL systems, "
       "starting air, exhaust, automation.",
    8: "Central ship systems -- ballast and bilge, fire fighting, wash down, "
       "electrical distribution.",
}
# Confidence: HIGH, quoted almost verbatim from the public description.
#
# THIS CORRECTS OUR OWN DEMO. tools/record-gap originally filed the lube oil
# events against a generator component in group 6. Lubricating oil is a SYSTEM,
# so it belongs in group 7. The distinction matters here more than anywhere
# else, because the whole causation argument turns on one LO system being common
# to three engines -- which is exactly what a group 7 code expresses and a
# group 6 code does not.

# HIGH: the code format. Three-digit group, then a three-digit suffix, split so
# that the suffix says what KIND of thing it is:
#   NNN.000 - NNN.099   Detail code   -- a component, bought direct to the ship
#   NNN.100 - NNN.999   Material code -- a spare, bought to stock
# The public example given is 731.000-731.099 and 731.100-731.999.
SFI_DETAIL_RANGE = (0, 99)
SFI_MATERIAL_RANGE = (100, 999)

# LOW -- and this is the honest part. Sources disagree on the actual subgroups.
# One says main group 6 -> group 60 "diesel engines for propulsion" -> subgroup
# 601 "diesel engines" -> 601001 "main diesel engine". Another shows 632.001 as
# "Main Engine". A third places 612/613 as high/medium-pressure steam turbines
# under "61 propulsion steam machinery", which is incompatible with the first.
#
# We cannot settle this without the licensed SFI manual. So the values below are
# SHAPED like SFI and are NOT SFI. They are marked so a reader corrects them
# rather than trusting them, and they are the single best thing to ask a
# superintendent or a SpecTec user to fix.
PLACEHOLDER_COMPONENTS = {
    "DG1": {"code": "6XX.001", "name": "Auxiliary engine no.1 (generator set)"},
    "DG2": {"code": "6XX.002", "name": "Auxiliary engine no.2 (generator set)"},
    "DG3": {"code": "6XX.003", "name": "Auxiliary engine no.3 (generator set)"},
    "TC1": {"code": "6XX.011", "name": "Turbocharger, auxiliary engine no.1"},
    "TC2": {"code": "6XX.012", "name": "Turbocharger, auxiliary engine no.2"},
    "TC3": {"code": "6XX.013", "name": "Turbocharger, auxiliary engine no.3"},
    "LO":  {"code": "7XX.001", "name": "Lubricating oil system, auxiliary engines"},
}
SFI_CONFIDENCE = "LOW -- structure is right, the digits are placeholders"


# --- What a PMS job record carries ------------------------------------------
# MEDIUM. Assembled from vendor descriptions (SpecTec AMOS, BASSnet, ShipNet,
# STAR Suite) and class guidance. Vendors describe these fields consistently;
# none of them publishes a schema, so field NAMES here are ours.

JOB_FIELDS = {
    "component_code": "SFI group + detail code. What the job is against",
    "job_code": "The maintenance task identifier within that component",
    "job_title": "Human description",
    "interval_type": "running_hours | calendar | condition | event",
    "interval_value": "e.g. 500 (hours) or 90 (days)",
    "due_rh": "Running hours at which it fell due",
    "done_rh": "Running-hour counter reading when carried out",
    "done_date": "Date carried out",
    "done_by": "Rank/person, and in practice the vessel, not the individual",
    "remarks": "FREE TEXT. The findings, the reason, the judgement",
    "order_no": "Link to purchase order or requisition, if parts were used",
    "criticality": "See below",
    "class_related": "Whether the job carries survey credit. See CMS below",
    "deferred": "Postponement, and normally who authorised it",
}

# The remarks field deserves special attention and is why this project exists.
# It is free text, it holds the reason and the finding, it is the least
# structured thing in the database and therefore the least portable -- and in
# the Gard turbocharger case it is precisely what was missing. Everything else
# survived in some form. Confidence: HIGH that it is free text and lossy;
# MEDIUM that it is the usual casualty of a migration.

INTERVAL_TYPES = ("running_hours", "calendar", "condition", "event")

CRITICALITY = {
    "critical": "Failure could cause a hazardous situation, loss of propulsion "
                "or steering, or a pollution event. Identified under the ISM "
                "Code and scrutinised in vetting inspections",
    "important": "Affects operation or class, not immediately hazardous",
    "routine": "Everything else",
}
# MEDIUM. ISM requires identification of equipment whose sudden operational
# failure may result in hazardous situations. The three-way split above is a
# common industry pattern, not a standard -- ASK ABOUT THIS.


# --- Why any of this is written down at all ---------------------------------
# This is the part that matters most and the part we understood least.

ISM_REQUIREMENT = (
    "The ISM Code requires the operator to establish a maintenance programme "
    "and keep records verifying the condition of the vessel and its equipment. "
    "A change of owner or manager triggers a new Document of Compliance and "
    "Safety Management Certificate -- but there is no consistent requirement "
    "that the historical records transfer with the ship. That asymmetry is the "
    "gap this project is about. Confidence: HIGH, stated by Gard 21 July 2026."
)

CMS_NOTE = (
    "Continuous Machinery Survey. Instead of a surveyor attending to open up "
    "machinery, class spreads machinery surveys over a five-year cycle. Under "
    "an APPROVED planned maintenance scheme, maintenance carried out and "
    "recorded on board under the chief engineer's responsibility EARNS SURVEY "
    "CREDIT for those items, with the class surveyor reviewing records and "
    "sampling completed jobs at periodic visits.\n\n"
    "The numbers are the interesting part. Around 85% of Lloyd's Register "
    "classed vessels are on a continuous survey cycle, but only around 15% "
    "have an approved Machinery Planned Maintenance Scheme -- 'even though "
    "virtually all operators are using computerised planned maintenance "
    "systems'.\n\n"
    "So: nearly everyone holds the data, and very few hold it in a form class "
    "will credit. Confidence: MEDIUM on the percentages, single source, and "
    "they are LR-specific. THEY ARE WORTH VERIFYING FIRST -- see README."
)


def component(key):
    """Placeholder component lookup. Raises loudly if asked for a real SFI code."""
    return PLACEHOLDER_COMPONENTS[key]


def summary():
    lines = ["SFI primary groups (confidence HIGH):"]
    for n, name in sorted(SFI_PRIMARY_GROUPS.items()):
        mark = "  <- lube oil lives here" if n == 7 else ""
        lines.append("  %d  %s%s" % (n, name, mark))
    lines.append("")
    lines.append("Component codes used by our demo: %s" % SFI_CONFIDENCE)
    lines.append("Job record fields modelled: %d" % len(JOB_FIELDS))
    lines.append("Criticality levels: %s" % ", ".join(CRITICALITY))
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
    print("\n--- CMS ---\n" + CMS_NOTE)
