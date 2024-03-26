# MLPerf Inference - Object Detection - KILT
This implementation runs image classification models with the KILT backend using the OnnxRT API on an Nvidia GPU.

Currently it supports the following models:
- retinanet

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

## Downloading Retinanet dependencies

Getting dataset:
1	Download openimages-mlperf.json	
```
axs byquery extracted,openimages_annotations,v2_1
```
2	Download Openimages Datasets Validation	
```
axs byquery downloaded,openimages_mlperf,validation+
```
3	Download Calibration Openimages Datasets	
```
axs byquery openimages_mlperf,calibration
```
4	Preprocess Calibration Datasets
```
axs byquery preprocessed,dataset_name=openimages,preprocess_method=pillow_torch,index_file=openimages_cal_images_list.txt,calibration+
```
5	Preprocess Full Openimages Datasets	
```
axs byquery preprocessed,dataset_name=openimages,preprocess_method=pillow_torch,first_n=24781,normalayout+
```

Compile the program binary
```
axs byquery compiled,kilt_executable,retinanet,device=onnxrt
```

Download model
```
axs byquery downloaded,onnx_model,model_name=retinanet,no_nms
```

## Benchmarking retinanet

Set backend to either CPU or GPU
```
export BACKEND=<cpu | gpu >
```

Set sut_name according to CPU/GPU
```
export SUT=<7920t-kilt-onnxruntime_cpu | 7920t-kilt-onnxruntime_gpu>
```

Set scenario
```
export SCENARIO=<SingleStream | MultiStream>
```

Measure Accuracy (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=object_detection,device=onnxrt,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=retinanet,loadgen_mode=AccuracyOnly , get accuracy
```

Measure Accuracy (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=object_detection,device=onnxrt,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=retinanet,loadgen_mode=AccuracyOnly,loadgen_dataset_size=24781,loadgen_buffer_size=64 , get accuracy
```

Run Performance (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=object_detection,device=onnxrt,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=retinanet,loadgen_mode=PerformanceOnly,loadgen_target_latency=1000 , parse_summary
```

Run Performance (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=object_detection,device=onnxrt,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=retinanet,loadgen_mode=PerformanceOnly,loadgen_dataset_size=24781,loadgen_buffer_size=64,loadgen_target_latency=<measured value> , parse_summary
```
