from pathlib import Path
import json, joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data/network_flows.csv"); X=df.drop(columns=["anomaly"]); y=df["anomaly"]
num=[c for c in X.columns if c!="protocol"]; cat=["protocol"]
pre=ColumnTransformer([("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),num),
                       ("cat",Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]),cat)])
pipe=Pipeline([("preprocess",pre),("classifier",LogisticRegression(max_iter=1200,class_weight="balanced"))])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y); pipe.fit(Xtr,ytr)
pred=pipe.predict(Xte); prob=pipe.predict_proba(Xte)[:,1]
m={"accuracy":float(accuracy_score(yte,pred)),"precision":float(precision_score(yte,pred,zero_division=0)),"recall":float(recall_score(yte,pred,zero_division=0)),"f1":float(f1_score(yte,pred,zero_division=0)),"roc_auc":float(roc_auc_score(yte,prob)),"confusion_matrix":confusion_matrix(yte,pred).tolist()}
joblib.dump(pipe,ROOT/"models/network_anomaly_pipeline.joblib"); (ROOT/"reports/metrics.json").write_text(json.dumps(m,indent=2)); print(json.dumps(m,indent=2))
