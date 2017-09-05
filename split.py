# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.params import TRAINING_DATA_RATIO
from ppg.utils import exist, load_json, dump_json, get_change_ratio


def split():
    extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')
    splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')

    if exist(pathname=extracted_data_dir):
        for filename_with_ext in fnmatch.filter(os.listdir(extracted_data_dir), '*.json'):
            feature_data = {
                '0': [],
                '1': [],
                '2': [],
            }
            pathname = os.path.join(extracted_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for session_id in json_data:
                    for block in json_data[session_id]['blocks']:
                        feature_data[str(block['level'])].append({
                            'ppg45': block['ppg']['ppg45'],
                            'ppg45_cr': get_change_ratio(data=block['ppg']['ppg45'], baseline=json_data[session_id]['rest']['ppg']['ppg45']),
                            'svri': block['ppg']['svri'],
                            'svri_cr': get_change_ratio(data=block['ppg']['svri'], baseline=json_data[session_id]['rest']['ppg']['svri']),
                        })
                output_data = {
                    'train': {
                        '0': feature_data['0'][:int(len(feature_data['0']) * TRAINING_DATA_RATIO)],
                        '1': feature_data['1'][:int(len(feature_data['1']) * TRAINING_DATA_RATIO)],
                        '2': feature_data['2'][:int(len(feature_data['2']) * TRAINING_DATA_RATIO)],
                    },
                    'test': {
                        '0': feature_data['0'][int(len(feature_data['0']) * TRAINING_DATA_RATIO):],
                        '1': feature_data['1'][int(len(feature_data['1']) * TRAINING_DATA_RATIO):],
                        '2': feature_data['2'][int(len(feature_data['2']) * TRAINING_DATA_RATIO):],
                    },
                }
                dump_json(data=output_data, pathname=os.path.join(splited_data_dir, filename_with_ext), overwrite=True)


if __name__ == '__main__':
    split()