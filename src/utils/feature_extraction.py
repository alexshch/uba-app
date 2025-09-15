import pandas as pd
import numpy as np

def extract_features(event_data):
    features = pd.DataFrame()

    features['auth_time'] = event_data['auth_time'].apply(lambda x: x.timestamp())
    features['user_ip'] = event_data['user_ip'].apply(lambda x: ip_to_numeric(x))
    features['server_ip'] = event_data['server_ip'].apply(lambda x: ip_to_numeric(x))
    features['command_count'] = event_data['commands'].apply(lambda x: len(x))
    features['service_count'] = event_data['services'].apply(lambda x: len(x))
    features['process_count'] = event_data['processes'].apply(lambda x: len(x))

    return features

def ip_to_numeric(ip):
    return int.from_bytes(map(int, ip.split('.')), 'big')