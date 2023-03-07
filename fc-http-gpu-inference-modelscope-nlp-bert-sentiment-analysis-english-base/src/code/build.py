from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.hub.snapshot_download import snapshot_download

# download BERT Model into ModelScope local cache
snapshot_download('damo/nlp_bert_sentiment-analysis_english-base', cache_dir='/tmp/model', revision='v1.0.0')
