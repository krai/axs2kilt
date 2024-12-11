# MLPerf Inference - Language Models - KILT
This implementation runs language models with the KILT backend using the OnnxRT API on an Nvidia GPU.

Currently it supports the following models:
- bert-99

## Setting up your environment
Start with a clean work_collection
```
axs byname work_collection , remove
```

Import these repos into your work_collection using SSH
```
axs byquery git_repo,collection,repo_name=axs2kilt-dev,url=git@github.com:krai/axs2kilt-dev.git
axs byquery git_repo,collection,repo_name=axs2onnxrt-dev,url=git@github.com:krai/axs2onnxrt-dev.git
axs byquery git_repo,collection,repo_name=axs2mlperf,url=git@github.com:krai/axs2mlperf.git
axs byquery git_repo,collection,repo_name=axs2qaic-dev,url=git@github.com:krai/axs2qaic-dev.git
axs byquery git_repo,repo_name=kilt-mlperf-dev,url=git@github.com:krai/kilt-mlperf-dev.git
```

Set Python version for compatibility
```
ln -s /usr/bin/python3.9 $HOME/bin/python3
```

Set Python version in axs 
```
axs byquery shell_tool,can_python
```

Get and extract onnxrt library
```
axs byquery extracted,onnxruntime_lib
```

## Downloading bert-99 dependencies

Compile protobuf
```
axs byquery compiled,protobuf
```

Download SQuad dataset, both variants
```
axs byquery preprocessed,dataset_name=squad_v1_1,calibration=no && axs byquery preprocessed,dataset_name=squad_v1_1,calibration=yes
```

Compile the program binary
```
axs byquery compiled,kilt_executable,bert,device=onnxrt
```

Download original base model
```
axs byquery onnx_conversion_ready,tf_model,model_name=bert_large
```

Convert original model to input-packed onnx model
```
axs byquery quant_ready,onnx_model,packed,model_name=bert_large
```

## Benchmarking bert-99

Set backend to either CPU or GPU
```
export BACKEND=<cpu | gpu >
```

Set sut_name according to CPU/GPU
```
export SUT=<7920t-kilt-onnxruntime_cpu | 7920t-kilt-onnxruntime_gpu>
```

Measure Accuracy (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=bert,device=onnxrt,backend_type=${BACKEND},framework=kilt,model_name=bert-99,loadgen_scenario=SingleStream,loadgen_mode=AccuracyOnly , get accuracy
```

Measure Accuracy (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=bert,device=onnxrt,backend_type=${BACKEND},framework=kilt,model_name=bert-99.9,loadgen_scenario=SingleStream,loadgen_mode=AccuracyOnly,loadgen_dataset_size=10833,loadgen_buffer_size=10833 , get accuracy
```

Run Performance (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=bert,device=onnxrt,backend_type=${BACKEND},framework=kilt,model_name=bert-99,loadgen_scenario=SingleStream,loadgen_mode=PerformanceOnly,loadgen_target_latency=1000 , parse_summary
```

Run Performance (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=bert,device=onnxrt,backend_type=${BACKEND},framework=kilt,model_name=bert-99,loadgen_scenario=SingleStream,loadgen_mode=PerformanceOnly,loadgen_dataset_size=10833,loadgen_buffer_size=10833,loadgen_target_latency=<measured value> , parse_summary
```
