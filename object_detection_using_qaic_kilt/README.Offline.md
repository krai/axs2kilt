# MLPerf Inference - Object Detection

## KILT - Qualcomm Cloud AI 100

### Offline

Define an Edge or a Datacenter SUT e.g. `export SUT=se450_q4_std` or `export SUT=dl385_q8_std`.

#### Accuracy
```
axs byquery loadgen_output,\
task=object_detection,model_name=retinanet,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=AccuracyOnly,\
loadgen_scenario=Offline\
 , get accuracy
```

#### Performance
```
axs byquery loadgen_output,\
task=object_detection,model_name=retinanet,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Offline,\
loadgen_compliance_test-\
 , parse_summary
```

#### Performance with Power
```
axs byquery power_loadgen_output,\
task=object_detection,model_name=retinanet,\
task=object_detection,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Offline,\
loadgen_compliance_test-\
 , get performance
```

#### Compliance

##### TEST01
```
axs byquery loadgen_output,\
task=object_detection,model_name=retinanet,\
task=object_detection,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Offline,\
loadgen_compliance_test=TEST01\
 , parse_summary
```

##### TEST05
```
axs byquery loadgen_output,\
task=object_detection,model_name=retinanet,\
framework=kilt,device=qaic,sut_name=${SUT},\
loadgen_mode=PerformanceOnly,\
loadgen_scenario=Offline,\
loadgen_compliance_test=TEST05\
 , parse_summary
```
