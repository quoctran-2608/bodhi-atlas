#!/usr/bin/env python3
"""Offline POC for a PROPOSED MITRA v3 PassageLink adapter.

All records are SYNTHETIC fixtures, not downloaded MITRA v3 data.
No API, ML, corpus download, human validation, or source reopen takes place.
"""
import hashlib
import json

SOURCE_REVISION = "SYNTHETIC_REV_A"
SOURCE_COMMIT = "NOT_A_REAL_COMMIT"

FIXTURES = [
    {"id": "SYN-001", "score": 0.86, "src_lang": "sa", "tgt_lang": "zh",
     "root_segnr": ["SA_SYN_A:1"], "par_segnr": ["ZH_SYN_A:1"],
     "root_segtext": ["anitya"], "par_segtext": ["無常"],
     "root_string": "anitya", "par_string": "無常", "root_length": 6, "par_length": 2},
    {"id": "SYN-002", "score": 0.76, "src_lang": "sa", "tgt_lang": "zh",
     "root_segnr": ["SA_SYN_A:2"], "par_segnr": ["ZH_SYN_A:2"],
     "root_segtext": ["duḥkha"], "par_segtext": ["苦"],
     "root_string": "duḥkha", "par_string": "苦", "root_length": 6, "par_length": 1},
    {"id": "SYN-NEG-001", "score": 0.99, "src_lang": "sa", "tgt_lang": "zh",
     "root_segnr": ["SA_SYN_A:3"], "par_segnr": ["ZH_SYN_A:3"],
     "root_segtext": ["anātman"], "par_segtext": ["常"],
     "root_string": "anātman", "par_string": "常", "root_length": 7, "par_length": 1},
]


def as_list(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, list) and v and all(isinstance(x, str) and x for x in v):
        return v
    raise ValueError("missing or malformed segment IDs")


def adapt(record, revision=SOURCE_REVISION):
    required = ("id", "score", "src_lang", "tgt_lang", "root_segnr", "par_segnr",
                "root_string", "par_string")
    missing = [k for k in required if k not in record]
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))
    roots = as_list(record["root_segnr"])
    pars = as_list(record["par_segnr"])
    if record["src_lang"] not in {"sa", "bo", "zh"} or record["tgt_lang"] not in {"sa", "bo", "zh"}:
        raise ValueError("language out of declared v3 scope")
    payload = json.dumps({
        "source_revision": revision, "source_record_id": str(record["id"]),
        "roots": roots, "pars": pars,
        "root_text": record["root_string"], "par_text": record["par_string"]
    }, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {
        "passage_link_id": "mitra:v3:" + hashlib.sha256(payload).hexdigest()[:20],
        "upstream_record_id": record["id"],
        "revision": revision,
        "src_lang": record["src_lang"], "tgt_lang": record["tgt_lang"],
        "src_segment_ids": roots, "tgt_segment_ids": pars,
        "relation_type": "ALIGNED_TRANSLATION_CANDIDATE",
        "score": record["score"], "score_semantics": "SPAN_DENSITY_NOT_PROBABILITY",
        "provenance": {"repo": "dharmamitra/mitra-parallel", "release": "v3",
                       "commit": SOURCE_COMMIT, "upstream_record_id": record["id"]},
        "status": "PROPOSED", "reviewer": None,
        "source_locator_status": "UNRESOLVED",
        "verification": {"text": "NOT_VERIFIED", "location": "NOT_VERIFIED", "meaning": "NOT_ASSESSED"},
        "citation_allowed": False,
    }


def main():
    out = [adapt(r) for r in FIXTURES]
    assert len(out) == 3
    assert len({r["passage_link_id"] for r in out}) == len(out)
    assert all(r["status"] == "PROPOSED" and not r["citation_allowed"] for r in out)
    assert out[2]["upstream_record_id"] == "SYN-NEG-001"
    assert adapt(FIXTURES[0])["passage_link_id"] == adapt(FIXTURES[0])["passage_link_id"]
    assert adapt(FIXTURES[0], revision="SYNTHETIC_REV_B")["passage_link_id"] != out[0]["passage_link_id"]
    bad = dict(FIXTURES[0]); bad.pop("root_segnr")
    try:
        adapt(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid source was accepted")
    print("environment=Python standard library; input=3 SYNTHETIC v3-shaped fixtures")
    print("adapter_output=3; proposed=3; verified=0; citation_allowed=0")
    print("negative_fixture=retained_as_PROPOSED; missing_ids=REJECTED")
    print("id_repeat_same_revision=STABLE; revision_change=NEW_ID_REQUIRES_CROSSWALK")
    print("real_v3_data_read=NO; source_reopen=NOT_TESTED; accuracy=NOT_MEASURED")


if __name__ == "__main__":
    main()
