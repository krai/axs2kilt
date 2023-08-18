# Generated file by scripts/custom_systems/add_custom_system.py                                                                                     [71/1953]# Contains configs for all custom systems in code/common/systems/custom_list.py

from . import *


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class CHAI(OfflineGPUBaseConfig):
    system = KnownSystem.Chai

    # Applicable fields for this benchmark are listed below. Not all of these are necessary, and some may be defined in the BaseConfig already and inherited.    # Please see NVIDIA's submission config files for example values and which fields to keep.
    # Required fields (Must be set or inherited to run):
    gpu_batch_size: int = 256
    input_dtype: str = 'int32'
    input_format: str = 'linear'
    precision: str = 'int8'
    tensor_path: str = 'build/preprocessed_data/squad_tokenized/input_ids.npy,build/preprocessed_data/squad_tokenized/segment_ids.npy,build/preprocessed_data/squad_tokenized/input_mask.npy'

    # Optional fields:
    active_sms: int = 0
    bert_opt_seqlen: int = 384
    buffer_manager_thread_count: int = 0
    cache_file: str = None
    coalesced_tensor: bool = True
    #deque_timeout_usec: int = 0
    enable_interleaved: bool = False
    #gemm_plugin_fairshare_cache_size: int = 0
    gpu_copy_streams: int = 1
    gpu_inference_streams: int = 1
    #graph_specs: str = None
    #graphs_max_seqlen: int = 0
    #instance_group_count: int = 0
    model_path: str = 'build/models/bert/bert_large_v1_1_fake_quant.onnx'
    numa_config: str = None
    offline_expected_qps: int = 5000
    performance_sample_count: int = 10833
    #performance_sample_count_override: int = 10833
    preferred_batch_size: str = None
    #request_timeout_usec: int = 0
    #run_infer_on_copy_streams: bool = False
    #soft_drop: float = 0.0
    use_fp8: bool = False
    use_graphs: bool = False
    use_jemalloc: bool = False
    use_small_tile_gemm_plugin: bool = True
    use_spin_wait: bool = False
    workspace_size: int = 2147483648


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)                                                                       class CHAI_HighAccuracy(CHAI):
    precision = "fp16"
    #offline_expected_qps = CHAI.offline_expected_qps / 2
    model_path: str = 'build/models/bert/bert_large_v1_1.onnx'


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)                                                                         class CHAI_Triton(CHAI):
    use_triton = True

    # Applicable fields for this benchmark are listed below. Not all of these are necessary, and some may be defined in the BaseConfig already and inherited.    # Please see NVIDIA's submission config files for example values and which fields to keep.
    # Required fields (Must be set or inherited to run):
    gpu_batch_size: int = 0
    input_dtype: str = ''
    input_format: str = ''
    precision: str = ''
    tensor_path: str = ''

    # Optional fields:
    active_sms: int = 0
    batch_triton_requests: bool = False
    bert_opt_seqlen: int = 0
    buffer_manager_thread_count: int = 0
    cache_file: str = ''
    coalesced_tensor: bool = False
    deque_timeout_usec: int = 0
    enable_interleaved: bool = False
    gather_kernel_buffer_threshold: int = 0
    gemm_plugin_fairshare_cache_size: int = 0
    gpu_copy_streams: int = 0
    gpu_inference_streams: int = 0
    graph_specs: str = ''
    graphs_max_seqlen: int = 0
    instance_group_count: int = 0
    max_queue_delay_usec: int = 0
    model_path: str = ''
    num_concurrent_batchers: int = 0
    num_concurrent_issuers: int = 0
    numa_config: str = ''
    offline_expected_qps: int = 0
    output_pinned_memory: bool = False
    performance_sample_count_override: int = 0
    preferred_batch_size: str = ''
    request_timeout_usec: int = 0
    run_infer_on_copy_streams: bool = False
    soft_drop: float = 0.0
    use_concurrent_harness: bool = False
    use_fp8: bool = False
    use_graphs: bool = False
    use_jemalloc: bool = False
    use_small_tile_gemm_plugin: bool = False
    use_spin_wait: bool = False
    workspace_size: int = 0


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class CHAI_HighAccuracy_Triton(CHAI_HighAccuracy):
    use_triton = True