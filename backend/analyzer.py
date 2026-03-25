import pandas as pd
import base64
from datetime import datetime, timedelta
import collections

class Analyzer:
    def __init__(self, data_dir, ddos_threshold=100):
        self.data_dir = data_dir
        self.nodes_df = pd.read_csv(f"{data_dir}/node_registry.csv")
        self.schemas_df = pd.read_csv(f"{data_dir}/schema_config.csv")
        self.logs_df = pd.read_csv(f"{data_dir}/system_logs.csv")
        self.ddos_threshold = ddos_threshold
        
        # We will hold state in-memory
        self.processed_data = []
        self.node_states = collections.defaultdict(list)
        self.node_risk = {}
        
        self.process_raw_data()
        
    def decode_serial(self, user_agent):
        try:
            encoded = str(user_agent).split(' ')[-1]
            return encoded, base64.b64decode(encoded).decode('utf-8')
        except:
            return None, None
            
    def get_schema_version(self, time_val):
        # time_start from schema_config.csv:
        # e.g. 1 at 0, 2 at 5000
        # sort by time_start descending
        schemas = self.schemas_df.sort_values(by="time_start", ascending=False)
        for _, row in schemas.iterrows():
            if time_val >= row['time_start']:
                return str(row['version'])
        return "1"

    def process_raw_data(self):
        # We will iterate through logs or do vectorized
        # To simulate a stream, we sort by log_id
        self.logs_df = self.logs_df.sort_values('log_id')
        
        # Pre-process nodes
        nodes_dict = {}
        for _, row in self.nodes_df.iterrows():
            encoded, decoded = self.decode_serial(row.get('user_agent', ''))
            nodes_dict[str(row['node_uuid'])] = {
                'encoded_serial': encoded,
                'decoded_serial': decoded,
            }
            
        base_time = datetime.utcnow() - timedelta(seconds=len(self.logs_df))
        
        # For anomalies, we need rolling average per node
        # latency window: last 10 requests? Let's say last 10.
        latency_history = collections.defaultdict(list)
        # ddos window: timestamps of requests
        request_history = collections.defaultdict(list)
        
        # We will build processing sequentially to properly detect spikes based on rolling avg
        for _, row in self.logs_df.iterrows():
            t_offset = row['log_id']
            curr_time = base_time + timedelta(seconds=t_offset)
            node_id = str(row['node_id'])
            latency = float(row['response_time_ms'])
            status_code = int(row['http_response_code'])
            
            schema_v = self.get_schema_version(t_offset)
            
            # Risk/Flags
            flags = []
            
            # Error
            if status_code >= 500:
                flags.append("error")
                
            # Latency Spike (> 2x rolling avg)
            hist = latency_history[node_id]
            if len(hist) >= 5:
                avg_lat = sum(hist) / len(hist)
                if latency > 2 * avg_lat:
                    flags.append("latency_spike")
            hist.append(latency)
            if len(hist) > 20:
                hist.pop(0)
                
            # DDOS (requests per node per minute > threshold)
            # We treat log_id as seconds. curr_time is exactly that.
            reqs = request_history[node_id]
            reqs.append(curr_time)
            # Remove requests older than 1 minute (60 seconds)
            while reqs and (curr_time - reqs[0]).total_seconds() > 60:
                reqs.pop(0)
                
            if len(reqs) > self.ddos_threshold:
                flags.append("ddos")
                
            # Node metadata
            n_meta = nodes_dict.get(node_id, {'encoded_serial': None, 'decoded_serial': None})
            
            item = {
                "node_id": node_id,
                "timestamp": curr_time.isoformat(),
                "latency": latency,
                "status_code": status_code,
                "schema_version": schema_v,
                "encoded_serial": n_meta['encoded_serial'],
                "decoded_serial": n_meta['decoded_serial'],
                "risk_score": 0.0, # calculate later or now
                "flags": flags
            }
            
            self.node_states[node_id].append(item)
            self.processed_data.append(item)
            
        # Compute Risk Score
        # Risk Score Combine: error_rate, latency_spikes, traffic_spikes (ddos)
        for node_id, states in self.node_states.items():
            errors = sum(1 for s in states if "error" in s["flags"])
            lat_spikes = sum(1 for s in states if "latency_spike" in s["flags"])
            ddos = sum(1 for s in states if "ddos" in s["flags"])
            
            total = len(states)
            if total == 0:
                risk = 0.0
            else:
                # normalize metrics
                error_rate = errors / total
                lat_rate = lat_spikes / total
                ddos_rate = ddos / total
                risk = (error_rate * 0.4 + lat_rate * 0.3 + ddos_rate * 0.3)
                risk = min(risk * 10, 1.0) # Scale up naturally to 0-1 range
            
            self.node_risk[node_id] = risk
            
            # update risk score in states
            for s in states:
                s["risk_score"] = risk
                
    def get_latest_data(self, limit=100):
        # sort processed data by timestamp desc
        return self.processed_data[-limit:]

    def get_nodes(self):
        # return latest node risk and status
        resp = []
        for node_id, r in self.node_risk.items():
            latest = self.node_states[node_id][-1]
            resp.append({
                "node_id": node_id,
                "risk_score": r,
                "is_online": True,
                "flags": latest["flags"],
                "last_latency": latest["latency"]
            })
        return resp
        
    def get_heatmap_data(self):
        # latency over time per node
        # we can subsample if too large
        points = []
        # taking last 1000 for heatmap
        for d in self.processed_data[-1000:]:
            points.append({
                "node_id": d["node_id"],
                "time": d["timestamp"],
                "latency": d["latency"]
            })
        return points
        
    def get_schemas(self):
        # schema version timeline
        points = []
        # aggregate schemas over time
        for d in self.processed_data[-1000:]:
            points.append({
                "time": d["timestamp"],
                "schema_version": d["schema_version"]
            })
        return points
        
    def get_assets(self):
        # set of decoded serials
        assets = []
        seen = set()
        for d in self.processed_data:
            s = d["decoded_serial"]
            if s and s not in seen:
                assets.append({"node_id": d["node_id"], "serial": s})
                seen.add(s)
        return assets
