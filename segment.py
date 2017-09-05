# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.params import PPG_SAMPLE_RATE
from ppg.utils import exist, load_text, dump_json


def segment():
    raw_ppg_data_dir = os.path.join(BASE_DIR, 'data', 'raw', 'ppg')
    segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')

    if exist(pathname=raw_ppg_data_dir):
        output_data = {}
        for filename_with_ext in fnmatch.filter(os.listdir(raw_ppg_data_dir), '*.txt'):
            filename, file_ext = os.path.splitext(filename_with_ext)
            if filename.endswith('-rest'):
                participant, session_id, block_id = filename.split('-')
                if participant not in output_data:
                    output_data[participant] = {}
                if session_id not in output_data[participant]:
                    output_data[participant][session_id] = {
                        'rest': {
                            'ppg': {},
                        },
                        'blocks': [],
                    }
                output_data[participant][session_id]['rest']['ppg']['sample_rate'] = PPG_SAMPLE_RATE
                output_data[participant][session_id]['rest']['ppg']['signal'] = map(float, load_text(pathname=os.path.join(raw_ppg_data_dir, filename_with_ext)))
            else:
                participant, session_id, block_id, task_level = filename.split('-')
                if participant not in output_data:
                    output_data[participant] = {}
                if session_id not in output_data[participant]:
                    output_data[participant][session_id] = {
                        'rest': {
                            'ppg': {},
                        },
                        'blocks': [],
                    }
                output_data[participant][session_id]['blocks'].append({
                    'level': task_level,
                    'ppg': {
                        'sample_rate': PPG_SAMPLE_RATE,
                        'signal': map(float, load_text(pathname=os.path.join(raw_ppg_data_dir, filename_with_ext))),
                    },
                })

        for participant in output_data:
            output_filename = '%s.json' % participant
            dump_json(data=output_data[participant], pathname=os.path.join(segmented_data_dir, output_filename), overwrite=True)


if __name__ == '__main__':
    segment()