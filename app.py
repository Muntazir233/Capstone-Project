import streamlit as st,pandas as pd,joblib
from pathlib import Path
model=joblib.load(Path(__file__).parent/"models/network_anomaly_pipeline.joblib")
st.set_page_config(page_title="Network Traffic Anomaly Detector",page_icon="🛡️",layout="wide")
st.title("🛡️ Adaptive Network Traffic Anomaly Detector"); st.caption("Educational prototype — predicts whether a network flow is normal or anomalous.")
with st.form("f"):
 c1,c2,c3=st.columns(3)
 with c1: duration=st.number_input("Flow duration (s)",.01,1000.,2.5); packets=st.number_input("Packet count",1,100000,55); bytes_=st.number_input("Byte count",200.,1e9,34000.)
 with c2: pr=st.number_input("Packet rate",.01,1e7,22.); br=st.number_input("Byte rate",.01,1e9,13000.); protocol=st.selectbox("Protocol",["TCP","UDP","ICMP"])
 with c3: src=st.number_input("Source port",1,65535,443); dst=st.number_input("Destination port",1,65535,443); entropy=st.number_input("Flow entropy",0.,10.,4.8)
 go=st.form_submit_button("Analyze flow")
if go:
 row=pd.DataFrame([{"flow_duration":duration,"packet_count":packets,"byte_count":bytes_,"packet_rate":pr,"byte_rate":br,"protocol":protocol,"src_port":src,"dst_port":dst,"flow_entropy":entropy}])
 p=float(model.predict_proba(row)[0,1]); pred=int(p>=.5)
 (st.error if pred else st.success)(f"Prediction: {'ANOMALOUS' if pred else 'NORMAL'} — risk score {p:.1%}"); st.progress(min(max(p,0),1)); st.dataframe(row,use_container_width=True)
