from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# Download the model files to the local cache
pipeline(Tasks.visual_grounding, model='damo/ofa_visual-grounding_refcoco_large_en')
