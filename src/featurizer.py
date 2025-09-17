# featurizer.py
from collections import Counter
import numpy as np
import re

COMMAND_TOK_RE = re.compile(r"[A-Za-z0-9_\-./@]+")

COMMON_SUSPICIOUS = ["scp","curl","wget","nc","ncat","python","bash -i","base64","tar","rm -rf","ssh"]

def tokenize_command(cmd: str):
    if not cmd: return []
    return COMMAND_TOK_RE.findall(cmd.lower())

def command_features(cmd: str):
    toks = tokenize_command(cmd)
    features = {}
    features["cmd_len"] = len(cmd) if cmd else 0
    features["tok_count"] = len(toks)
    for s in COMMON_SUSPICIOUS:
        features[f"has_{s.replace(' ','_')}"] = 1 if s in cmd.lower() else 0
    return features

def session_features(session):
    """
    session: { session_id, user, host, events: [ ... ], start, end, duration_sec }
    returns dict of features
    """
    evs = session["events"]
    feats = {}
    feats["user"] = session["user"]
    feats["host"] = session["host"]
    feats["duration_sec"] = session.get("duration_sec",0)
    feats["n_events"] = len(evs)
    # commands aggregate
    cmd_lens = [len(e.get("command") or "") for e in evs]
    feats["avg_cmd_len"] = float(np.mean(cmd_lens)) if cmd_lens else 0.0
    feats["max_cmd_len"] = float(max(cmd_lens)) if cmd_lens else 0.0
    feats["n_sudo"] = sum(1 for e in evs if "sudo" in (e.get("command") or "").lower())
    feats["n_failed_cmds"] = sum(1 for e in evs if e.get("exit_code",0)!=0)
    feats["n_distinct_commands"] = len(set(e.get("command") for e in evs))
    feats["n_auth_failures"] = sum(1 for e in evs if e.get("auth_result")=="failure")
    feats["n_pubkey_auth"] = sum(1 for e in evs if e.get("auth_method")=="publickey")
    feats["n_password_auth"] = sum(1 for e in evs if e.get("auth_method")=="password")
    feats["has_target_root"] = int(any(e.get("target_account")=="root" for e in evs))
    feats["any_exfil_cmd"] = int(any(k for e in evs for k in COMMON_SUSPICIOUS if k in (e.get("command") or "").lower()))
    feats["n_night_events"] = sum(1 for e in evs if e.get("_is_night"))
    # token bag features (top-k)
    toks = Counter()
    for e in evs:
        toks.update(tokenize_command(e.get("command") or ""))
    # take top 10 tokens of session
    top_tokens = [t for t,_ in toks.most_common(10)]
    for i,t in enumerate(top_tokens):
        feats[f"token_{i}"] = t
    # fallback zeros for token_i up to 10
    for i in range(10):
        feats.setdefault(f"token_{i}", "")
    return feats

def vectorize_sessions(sessions):
    """
    Convert list of session feature dicts into X matrix and metadata.
    For simplicity, we encode categorical tokens and user via simple hashing.
    """
    rows = []
    metas = []
    for s in sessions:
        f = session_features(s)
        metas.append({"session_id": s["session_id"], "user": f["user"], "host": f["host"]})
        # numeric vector: choose numeric features + hash tokens + n_events etc.
        vec = [
            f["duration_sec"],
            f["n_events"],
            f["avg_cmd_len"],
            f["max_cmd_len"],
            f["n_sudo"],
            f["n_failed_cmds"],
            f["n_distinct_commands"],
            f["n_auth_failures"],
            f["n_pubkey_auth"],
            f["n_password_auth"],
            f["has_target_root"],
            f["any_exfil_cmd"],
            f["n_night_events"]
        ]
        # token hash features: map token -> small numeric via builtin hash
        for i in range(10):
            t = f.get(f"token_{i}") or ""
            vec.append( (hash(t) % 997) / 997.0 )  # simple stable numericization
        rows.append(vec)
    import numpy as np
    return np.array(rows, dtype=float), metas
