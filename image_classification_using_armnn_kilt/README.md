# MLPerf Inference - Image Classification - KILT
This implementation runs image classification models with the KILT backend using the Armnn API on an Nvidia GPU.

Currently it supports the following models:
- resnet50

## Setting up your environment
Start with a clean work_collection
```
axs byname work_collection , remove
```

Import these repos into your work_collection using SSH
```
axs byquery git_repo,collection,repo_name=axs2kilt-dev,url=git@github.com:krai/axs2kilt-dev.git
axs byquery git_repo,collection,repo_name=axs2armnn-dev,url=git@github.com:krai/axs2armnn-dev.git
axs byquery git_repo,collection,repo_name=axs2qaic-dev,url=git@github.com:krai/axs2armnn-dev.git
axs byquery git_repo,collection,repo_name=axs2mlperf,url=git@github.com:krai/axs2mlperf.git
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

Get and extract armnn library (add architecture=x86_64 for x86_64 machines)
```
axs byquery extracted,armnn_lib
```

## Downloading Resnet dependencies

Download full dataset
```
axs byname extractor , extract --archive_path=/datasets/dataset-imagenet-ilsvrc2012-val.tar --tags,=extracted,imagenet --strip_components=1 --dataset_size=50000
```

Compile the program binary
```
axs byquery compiled,kilt_executable,resnet50,device=armnn
```

EITHER: Generate the tflite model from the .pb model
```
axs byquery inference_ready,tf_model,model_name=resnet50
axs byquery tf_model,shape_fixed,model_name=resnet50
axs byquery tflite_model,pb2tflite,model_name=resnet50
```

OR: Download the pre-generated tflite model
```
axs byquery tflite_model,downloaded,model_name=resnet50
```

## Benchmarking resnet50

Set backend to either CpuRef (Reference C++ Kernels), CpuAcc (NEON) (currently degraded accuracy), or GpuAcc (OpenCl)
```
export BACKEND=<CpuRef | CpuAcc | GpuAcc >
```

Set sut_name
```
export SUT=<firefly_cpu | firefly_gpu>
```

Set scenario
```
export SCENARIO=<SingleStream | MultiStream>
```

Measure Accuracy (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=image_classification,device=armnn,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=resnet50,loadgen_mode=AccuracyOnly , get accuracy
```

Measure Accuracy (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=image_classification,device=armnn,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=resnet50,loadgen_mode=AccuracyOnly,loadgen_dataset_size=50000,loadgen_buffer_size=1024 , get accuracy
```

Run Performance (Quick Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=image_classification,device=armnn,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=resnet50,loadgen_mode=PerformanceOnly,loadgen_target_latency=1000 , parse_summary
```

Run Performance (Full Run)
```
axs byquery sut_name=${SUT},loadgen_output,task=image_classification,device=armnn,backend_type=${BACKEND},loadgen_scenario=${SCENARIO},framework=kilt,model_name=resnet50,loadgen_mode=PerformanceOnly,loadgen_dataset_size=50000,loadgen_buffer_size=1024,loadgen_target_latency=<measured value> , parse_summary
```
