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
        total_logs = len(self.processed_data)
        active_threats = 0

        dashboard_nodes = []
        import random
        
        for node_id, states in self.node_states.items():
            if not states: continue
            
            latest = states[-1]
            errors = sum(1 for s in states if "error" in s["flags"])
            lat_spikes = sum(1 for s in states if "latency_spike" in s["flags"])
            ddos = sum(1 for s in states if "ddos" in s["flags"])
            
            is_infected = (errors > 0 or lat_spikes > 0 or ddos > 0)
            
            # Conflict Detect
            last_status = latest.get("json_status", "OPERATIONAL") # Stub out if not in dataset
            last_code = latest["status_code"]
            conflict_detected = (str(last_status).upper() == "OPERATIONAL" and last_code >= 400)
                
            if is_infected or conflict_detected:
                active_threats += 1
                
            x_pos = random.random()
            y_pos = random.random()
            
            dashboard_nodes.append({
                "id": node_id,
                "pos": {"x": x_pos, "y": y_pos},
                "is_infected": is_infected,
                "conflict_detected": conflict_detected,
                "last_http_code": last_code,
                "reported_json": last_status,
                "decoded_serial": latest["decoded_serial"] if latest["decoded_serial"] else "UNKNOWN",
                "encoded_ua": latest["encoded_serial"] if latest["encoded_serial"] else "UNKNOWN"
            })
            
        self.dashboard_nodes = dashboard_nodes
        self.metadata = {
            "system_time": int(datetime.utcnow().timestamp()),
            "total_logs_processed": total_logs,
            "active_threats": active_threats,
            "status": "CRITICAL" if active_threats > 0 else "OPERATIONAL"
        }
                
    def get_dashboard_data(self):
        timestamps = []
        avg_latency = []
        anomaly_points = []
        
        times = collections.defaultdict(list)
        for d in self.processed_data[-500:]:
            ts = d["timestamp"]
            times[ts].append(d["latency"])
            if "latency_spike" in d["flags"]:
                anomaly_points.append({"timestamp": ts, "latency": d["latency"], "node_id": d["node_id"]})
        
        for ts in sorted(times.keys()):
            timestamps.append(ts)
            avg_latency.append(sum(times[ts]) / len(times[ts]))

        terminal_logs = []
        for d in self.processed_data[-100:]:
            terminal_logs.append(f"HTTP {d['status_code']} | Latency: {d['latency']:.1f}ms | Node: {d['node_id']}")

        latest_schema = self.get_schema_version(len(self.processed_data))
        
        return {
            "metadata": self.metadata,
            "schema_engine": {
                "current_version": int(latest_schema) if str(latest_schema).isdigit() else 1,
                "active_column": "L_V1",
                "rotation_timer": "600s",
                "sync_status": "SYNCED"
            },
            "nodes": self.dashboard_nodes,
            "heatmap_data": {
                "timestamps": timestamps,
                "avg_latency": avg_latency,
                "anomaly_points": anomaly_points
            },
            "live_terminal_logs": terminal_logs
        }
