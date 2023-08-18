# MLPerf Inference - Language Models - KILT
This implementation runs language models with the KILT backend using TensorRT API on a Nvidia GPU.
The inference is run on serialized engines generated with the NVisia toolset (dateils below).

Currently it supports the following models:
- bert-99
- bert-99.9

## Setting up your environment
Start with a clean work_collection
```
axs byname work_collection , remove
```

Import this repos into your work_collection
```
axs byquery git_repo,collection,repo_name=axs2tensorrt
axs byquery git_repo,collection,repo_name=axs2kilt
axs byquery git_repo,collection,repo_name=axs2tensorrt
axs byquery git_repo,collection,repo_name=axs2kilt
axs byquery git_repo,collection,repo_name=axs2mlperf
axs byquery git_repo,repo_name=kilt-mlperf
```

Set Python version for compatibility
```
ln -s /usr/bin/python3.9 $HOME/bin/python3
```

Set Python version in axs 
```
axs byquery shell_tool,can_python
```

## Downloading BERT dependencies

Compile protobuf 
```
axs byquery compiled,protobuf
```

Compile the program binary
```
axs byquery compiled,kilt_executable,bert,device=tensorrt
```

Set up a docker container for running NVidia submissions (https://github.com/mlcommons/inference_results_v3.0/tree/main/closed/NVIDIA). And use it to generate engines with provided custom configs, that are available at axs2kilt/bert_squad_kilt_loadgen_tensorrt/config/. Before generating engine ensure that the TensorRT version inside the container is the same as shown in the requrements (8.6.1).

Copy the resulting engines (one for the Offline scenatio, anothe one - for the Server scenario) into your work_collection.
```
scp ... ~/work_collection/tensorrt_bert_model/
```

## Benchmarking BERT-99

Measure Accuracy
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99,loadgen_scenario=Offline,loadgen_mode=AccuracyOnly , get accuracy
```

Run Performance (Quick Run)
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99,loadgen_scenario=Offline,loadgen_mode=PerformanceOnly,loadgen_target_qps=1 , parse_summary
```

Run Performance (Full Run)
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99,loadgen_scenario=Offline,loadgen_mode=PerformanceOnly,loadgen_dataset_size=10833,loadgen_buffer_size=10833,loadgen_target_qps=<measured value> , parse_summary
```


## Benchmarking BERT-99.9
Measure Accuracy
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99.9,loadgen_scenario=Offline,loadgen_mode=AccuracyOnly , get accuracy
```

Run Performance (Quick Run)
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99.9,loadgen_scenario=Offline,loadgen_mode=PerformanceOnly,loadgen_target_qps=1 , parse_summary
```


Run Performance (Full Run)
```
axs byquery sut_name=7920t-kilt-tensorrt,loadgen_output,bert_squad,device=tensorrt,framework=kilt,model_name=bert-99.9,loadgen_scenario=Offline,loadgen_mode=PerformanceOnly,loadgen_dataset_size=10833,loadgen_buffer_size=10833,loadgen_target_qps=<measured value> , parse_summary
```
