from typing import List, Tuple

import os
import csv

import numpy as np

from hatecomp.base.dataset import _HateDataset
from hatecomp.datasets.HASOC.download import HASOCDownloader, DEFAULT_DIRECTORY

class HASOCDataset(_HateDataset):
    __name__ = 'HASOC'
    downloader = HASOCDownloader

    TSV_FILES = [
        'english_dataset/english_dataset.tsv',
        'english_dataset/hasoc2019_en_test-2919.tsv'
    ]
    ENCODING_KEY = {
        'HOF' : 1,
        'NOT' : 0,
        'HATE' : 1,
        'OFFN' : 2,
        'PRFN' : 3,
        'TIN' : 1,
        'UNT' : 2,
        'NONE' : 0
    }

    def __init__(
        self,
        path = None,
        one_hot = True
    ):
        self.one_hot = one_hot
        super(HASOCDataset, self).__init__(path = path)
        
    def _load_data(self, path: str) -> Tuple[List]:
        returns = ([], [], [])
        for tsv_file in HASOCDataset.TSV_FILES:
            tsv_path = os.path.join(path, tsv_file)
            tsv = self._read_tsv(tsv_path)
            returns = returns + self._convert_tsv(tsv)
        return returns

    def _read_tsv(self, path: str) -> List[List[str]]:
        with open(path) as file:
            return list(csv.reader(file, delimiter = '\t'))

    def _convert_tsv(self, tsv: List[List[str]]) -> Tuple[List]:
        ids = []
        data = []
        labels = []
        for row in tsv[1:]:
            ids.append(row[0])
            data.append(row[1])
            labels.append([HASOCDataset.ENCODING_KEY[encoding] for encoding in row[2:]])
        return (np.array(data_list) for data_list in [ids, data, labels])