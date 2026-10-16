"""Rank unusual federal award amounts for human review, never as fraud findings."""
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd,joblib
from sklearn.ensemble import IsolationForest
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",required=True);p.add_argument("--amount",default="federal_action_obligation");p.add_argument("--group",default="awarding_agency_name");p.add_argument("--contamination",type=float,default=.01);p.add_argument("--out",default="outputs");a=p.parse_args()
 d=pd.read_csv(a.input,low_memory=False);d[a.amount]=pd.to_numeric(d[a.amount],errors="coerce");d=d.dropna(subset=[a.amount]).copy();d=d[d[a.amount]>=0]
 d["log_amount"]=np.log1p(d[a.amount]);features=["log_amount"]
 for c in [a.group,"award_type_code"]:
  if c in d:
   # Frequency encoding is fit on this analysis file; rerun against a frozen reference for deployment.
   freq=d[c].fillna("UNKNOWN").value_counts(normalize=True);d[c+"_frequency"]=d[c].fillna("UNKNOWN").map(freq);features.append(c+"_frequency")
 model=IsolationForest(n_estimators=300,contamination=a.contamination,random_state=42,n_jobs=-1);model.fit(d[features]);d["anomaly_score"]=-model.score_samples(d[features]);d["review_flag"]=model.predict(d[features])==-1
 cols=[c for c in ["award_id","recipient_name",a.group,a.amount] if c in d]+features+["anomaly_score","review_flag"]
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);d.sort_values("anomaly_score",ascending=False)[cols].to_csv(out/"review_queue.csv",index=False)
 summary={"records":len(d),"flagged":int(d.review_flag.sum()),"contamination":a.contamination,"warning":"Statistical outliers are not evidence of waste, abuse, or fraud."}
 (out/"summary.json").write_text(json.dumps(summary,indent=2));joblib.dump({"model":model,"features":features,"group_frequency":freq.to_dict() if a.group in d else {}},out/"model.joblib");print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
