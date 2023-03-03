from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.hub.snapshot_download import snapshot_download

# Download model
snapshot_download('damo/ofa_visual-grounding_refcoco_large_en', cache_dir='/tmp/model', revision='v1.0.0')
