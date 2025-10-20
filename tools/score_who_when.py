from __future__ import annotations
import argparse, json, os
from typing import Dict, List, Tuple
from collections import defaultdict, Counter

ALLOWED_WHO = ["tool", "model", "env"]
ALLOWED_WHEN = ["plan", "toolcall", "reflect", "final"]

def load_jsonl(path: str) -> List[dict]:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            if ln.strip():
                data.append(json.loads(ln))
    return data

def confusion(labels: List[str], preds: List[str], classes: List[str]):
    idx = {c:i for i,c in enumerate(classes)}
    m = [[0 for _ in classes] for _ in classes]  # gold x pred
    for y, yhat in zip(labels, preds):
        if y not in idx or yhat not in idx: continue
        m[idx[y]][idx[yhat]] += 1
    return m

def macro_f1(labels: List[str], preds: List[str], classes: List[str]) -> float:
    idx = {c:i for i,c in enumerate(classes)}
    tp = Counter()
    fp = Counter()
    fn = Counter()
    for y, yhat in zip(labels, preds):
        if yhat == y:
            tp[y] += 1
        else:
            fp[yhat] += 1
            fn[y] += 1
    f1s = []
    for c in classes:
        t = tp[c]; f_p = fp[c]; f_n = fn[c]
        prec = t / (t + f_p) if (t + f_p) > 0 else 0.0
        rec  = t / (t + f_n) if (t + f_n) > 0 else 0.0
        f1 = (2*prec*rec)/(prec+rec) if (prec+rec) > 0 else 0.0
        f1s.append(f1)
    return sum(f1s)/len(classes)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    gold = load_jsonl(args.gold)
    pred = load_jsonl(args.pred)
    gmap = {r.get("id") or r.get("instance_id") or r.get("qid"): r for r in gold}
    pmap = {r.get("id") or r.get("instance_id") or r.get("qid"): r for r in pred}

    y_who, yhat_who = [], []
    y_when, yhat_when = [], []
    kept = 0
    for k, g in gmap.items():
        if k not in pmap: continue
        p = pmap[k]
        gw = g.get("label_who") or g.get("who")
        gw = str(gw).strip().lower()
        gw = {"environment":"env"}.get(gw, gw)
        gw = gw if gw in ALLOWED_WHO else "model"

        gwm = g.get("label_when") or g.get("when")
        gwm = str(gwm).strip().lower()
        norm_when = {"planning":"plan","tool_call":"toolcall","tool-call":"toolcall","final_answer":"final"}
        gwm = norm_when.get(gwm, gwm)
        gwm = gwm if gwm in ALLOWED_WHEN else "final"

        pw = p.get("who_pred", "model")
        pm = p.get("when_pred", "final")

        y_who.append(gw); yhat_who.append(pw)
        y_when.append(gwm); yhat_when.append(pm)
        kept += 1

    who_acc = sum(1 for a,b in zip(y_who, yhat_who) if a==b) / max(1, len(y_who))
    when_acc = sum(1 for a,b in zip(y_when, yhat_when) if a==b) / max(1, len(y_when))
    joint_acc = sum(1 for i in range(len(y_who)) if y_who[i]==yhat_who[i] and y_when[i]==yhat_when[i]) / max(1, len(y_who))

    who_cm = confusion(y_who, yhat_who, ALLOWED_WHO)
    when_cm = confusion(y_when, yhat_when, ALLOWED_WHEN)

    who_f1 = macro_f1(y_who, yhat_who, ALLOWED_WHO)
    when_f1 = macro_f1(y_when, yhat_when, ALLOWED_WHEN)

    out = {
        "num_examples": kept,
        "who_acc": who_acc,
        "who_macro_f1": who_f1,
        "when_acc": when_acc,
        "when_macro_f1": when_f1,
        "joint_acc": joint_acc,
        "who_confusion": {
            "labels": ALLOWED_WHO, "matrix": who_cm
        },
        "when_confusion": {
            "labels": ALLOWED_WHEN, "matrix": when_cm
        }
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
