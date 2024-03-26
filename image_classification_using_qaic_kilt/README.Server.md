# MLPerf Inference - Image Classification

## KILT - Qualcomm Cloud AI 100

### Server

Define a Datacenter SUT e.g. `export SUT=dl385_q8_std`.

#### Accuracy
```
axs byquery loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=AccuracyOnly,\
loadgen_scenario=Server\
 ,  get accuracy
```

#### Performance
```
axs byquery loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Server,\
loadgen_compliance_test-\
 , parse_summary
```

#### Performance with Power
```
axs byquery power_loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Server,\
loadgen_compliance_test-\
 , parse_summary
```

#### Compliance

##### TEST01
```
axs byquery loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Server,\
loadgen_compliance_test=TEST01\
 , parse_summary
```

##### TEST04
```
axs byquery loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Server,\
loadgen_compliance_test=TEST04\
 , parse_summary
```

##### TEST05
```
axs byquery loadgen_output,\
task=image_classification,model_name=resnet50,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Server,\
loadgen_compliance_test=TEST05\
 , parse_summary
```
