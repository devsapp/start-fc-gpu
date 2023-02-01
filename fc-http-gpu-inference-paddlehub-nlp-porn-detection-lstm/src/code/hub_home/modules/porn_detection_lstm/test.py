# -*- coding:utf-8 -*-
from __future__ import print_function

import json
import six

import paddlehub as hub

if __name__ == "__main__":
    # Load porn_detection module
    porn_detection_lstm = hub.Module(name="porn_detection_lstm")

    test_text = ["黄片下载", "打击黄牛党"]

    input_dict = {"text": test_text}
    results = porn_detection_lstm.detection(
        data=input_dict, use_gpu=True, batch_size=1)
    for index, result in enumerate(results):
        if six.PY2:
            print(json.dumps(
                results[index], encoding="utf8", ensure_ascii=False))
        else:
            print(results[index])

    results = porn_detection_lstm.detection(
        texts=test_text, use_gpu=False, batch_size=2)
    for index, result in enumerate(results):
        if six.PY2:
            print(json.dumps(
                results[index], encoding="utf8", ensure_ascii=False))
        else:
            print(results[index])

    print(porn_detection_lstm.get_vocab_path())
    print(porn_detection_lstm.get_labels())
