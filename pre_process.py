#%%
import os
import copy as cp
from constants import *
from utils.utils import *

file_statements_metrics_name = 'statements_and_metrics_UNSEEN_PROJECTED.json'
file_orig_data = 'TO_PROJECT.json'
file_gen_data0 = 'xxx.json'
file_gen_data1 = 'yyy.json'

path_to_file = os.path.join(DATA_PATH, file_statements_metrics_name)
statements_metrics = load_data(path_to_file)

path_to_file = os.path.join(DATA_PATH, file_orig_data)
orig_data = load_data(path_to_file)

path_to_file = os.path.join(DATA_PATH, file_gen_data0)
gen_data0 = load_data(path_to_file)
path_to_file = os.path.join(DATA_PATH, file_gen_data1)
gen_data1 = load_data(path_to_file)

gen_data = gen_data0 + gen_data1

statements_metrics_cp = cp.deepcopy(statements_metrics)

# we take the prediction and find what are the original uuid to get then the labels
for i, sm in enumerate(statements_metrics):
    src_encoded = sm['src'] # the prediction has been performed using the uuid in the Platform (different from the uuid generated creating data)
    dest_encoded = sm['dest']
    
    for orig_datum in orig_data:
        if 'uuid' in orig_datum and src_encoded == orig_datum['uuid']:
            statements_metrics_cp[i]['src_orig'] = orig_datum['Original UUID']
            for g in gen_data:
                if 'uuid' in g and g['uuid'] == orig_datum['Original UUID']:
                        statements_metrics_cp[i]['src_label'] = g['label']
                        break
                        
        if 'uuid' in orig_datum and dest_encoded == orig_datum['uuid']:
            statements_metrics_cp[i]['dest_orig'] = orig_datum['Original UUID']
            for g in gen_data:
                if 'uuid' in g and g['uuid'] == orig_datum['Original UUID']:
                        statements_metrics_cp[i]['dest_label'] = g['label']
                        break
                    
path_to_file = os.path.join(DATA_PATH, file_statements_metrics_name[:-5]+'_mod.json')
save_data(path_to_file, statements_metrics_cp)