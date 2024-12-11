import copy
import os
import struct
from collections import Counter
from dataclasses import dataclass

import numpy as np
import pint
import tabulate

MAX_INT_64 = 9_223_372_036_854_775_807

@dataclass
class Event:
    start_ns: int
    end_ns: int
    tid: int
    name: str
    batch_id: int
    on_device: bool
    is_long_event: bool
    is_counter_event: bool
    counter_value: int = 0


def enable_chaining(func):
    setattr(Trace, func.__name__, func)
    return func

class Trace:
    _reverse_name_dict: dict = {}

    def __init__(self, __entry__) -> None:
        self.__entry__ = __entry__

    # Generator function that yields global events
    def global_events(self):
        assert False, "unreachable"

    # Generator function that yields events that occured on device_id
    def device_events(self, device_id):
        assert False, "unreachable"

    # Returns all device_ids
    def devices(self):
        assert False, "unreachable"

    def save(self, filename: str):
        path = os.path.join(self.__entry__.get("abs_dir"), filename)
        with open(path, "wb") as file:
            file.write(struct.pack("<I", len(self._name_dict)))

            for id_value, string in self._name_dict.items():
                file.write(f"{string}\0".encode("utf-8"))
                file.write(struct.pack("<I", id_value))

            global_events = list(self.global_events())
            file.write(struct.pack("<I", len(global_events)))

            for event in self.global_events():
                file.write(
                    struct.pack(
                        "<qqIxxxxqi?xxx",
                        event.start_ns,
                        event.end_ns,
                        self._reverse_name_dict[event.name],
                        event.tid,
                        event.batch_id,
                        event.is_long_event,
                    )
                )

            del global_events

            device_events = {}
            for device_id in self.devices():
                device_events[device_id] = list(
                    map(copy.deepcopy, self.device_events(device_id))
                )
            file.write(struct.pack("<I", len(device_events)))

            for device_id, events in device_events.items():
                file.write(struct.pack("<I", device_id))
                file.write(struct.pack("<I", len(events)))

                for event in events:
                    file.write(
                        struct.pack(
                            "<qqIxxxxi?xxx",
                            event.start_ns,
                            event.end_ns,
                            self._reverse_name_dict[event.name],
                            event.batch_id,
                            event.is_long_event,
                        )
                    )
        return path


class TraceReader(Trace):
    _GLOBAL_EVENT_SIZE = 40
    _DEVICE_EVENT_SIZE = 32

    def __init__(self, filename: str, __entry__) -> None:
        super().__init__(__entry__)
        self._file = open(filename, "rb")
        self._read_metadata()
        self._global_event_buffer = bytearray(self._GLOBAL_EVENT_SIZE)
        self._device_event_buffer = bytearray(self._DEVICE_EVENT_SIZE)
        self._event = Event(0, 0, 0, "", 0, False, False, False)

    def _read_header(self):
        data = {}
        # Read the number of strings (uint32_t)
        n_strings_data = self._file.read(4)
        if not n_strings_data:
            raise Exception("Malformed header - n_strings")

        n_strings = struct.unpack("<I", n_strings_data)[0]

        # Read the strings and IDs
        for _ in range(n_strings):
            # Read null-terminated string
            string = b""
            char = b""
            while char != b"\x00":
                string += char
                char = self._file.read(1)

            # Read ID (uint32_t)
            id_data = self._file.read(4)
            if not id_data:
                raise Exception("Malformed header")
            id_value = struct.unpack("<I", id_data)[0]

            data[id_value] = string.decode("utf-8")

        return data

    def _read_metadata(self):
        self._name_dict = self._read_header()
        self._reverse_name_dict = {v: k for k, v in self._name_dict.items()}

        # Read the number of events (uint32_t)
        num_events_data = self._file.read(4)
        if not num_events_data:
            raise ValueError("File not formatted correctly - nothing after header")
        self._n_global_events = struct.unpack("<I", num_events_data)[0]
        self._global_events_start = self._file.tell()

        self._file.seek(self._n_global_events * self._GLOBAL_EVENT_SIZE, 1)
        num_devices_data = self._file.read(4)
        if not num_devices_data:
            return
        self._n_devices = struct.unpack("<I", num_devices_data)[0]
        self._device_event_positions = {}

        for _ in range(self._n_devices):
            device_id_data = self._file.read(4)
            if not device_id_data:
                raise Exception("Malformed buffer events (device_id = unknown)")
            device_id = struct.unpack("<I", device_id_data)[0]

            # Read number of events (uint32_t)
            num_events_data = self._file.read(4)
            if not num_events_data:
                raise Exception(f"Malformed buffer events (device_id = {device_id})")
            num_events = struct.unpack("<I", num_events_data)[0]

            self._device_event_positions[device_id] = (self._file.tell(), num_events)
            self._file.seek(num_events * self._DEVICE_EVENT_SIZE, 1)

    def global_events(self):
        self._file.seek(self._global_events_start)
        self._event.on_device = False
        for _ in range(self._n_global_events):
            # Read start_ns (int64_t), end_ns (int64_t), id (uint32_t), tid (uint64_t), batch_id (uint32_t)
            event_data = self._file.readinto(self._global_event_buffer)
            if not event_data:
                raise Exception("Malformed event")

            start_ns, end_ns, id_value, tid, batch_id, is_long_event, is_counter_event = struct.unpack(
                "<qqIxxxxqi??xx", self._global_event_buffer
            )
            self._event.start_ns = start_ns
            self._event.end_ns = end_ns
            self._event.tid = tid
            self._event.name = self._name_dict[id_value]
            self._event.batch_id = batch_id
            self._event.is_long_event = is_long_event
            self._event.is_counter_event = is_counter_event
            self._event.counter_value = end_ns

            yield self._event

    def devices(self):
        return self._device_event_positions.keys()

    def device_events(self, device_id):
        start_loc, n_events = self._device_event_positions[device_id]
        self._file.seek(start_loc)

        self._event.tid = device_id
        self._event.on_device = True
        for _ in range(n_events):
            # Read start_ns (int64_t), end_ns (int64_t), id (uint32_t), blank (uint32_t), batch_id (uint32_t)
            event_data = self._file.readinto(self._device_event_buffer)
            if not event_data:
                raise Exception(f"Malformed buffer events (device_id = {device_id})")

            (
                self._event.start_ns,
                self._event.end_ns,
                id_value,
                self._event.batch_id,
                self._event.is_long_event,
                self._event.is_counter_event
            ) = struct.unpack("<qqIxxxxi??xx", self._device_event_buffer)

            self._event.name = self._name_dict[id_value]
            self._event.counter_value = self._event.end_ns

            yield self._event

    def __del__(self):
        self._file.close()


class TraceFilterer(Trace):
    def __init__(self, trace: Trace) -> None:
        super().__init__(trace.__entry__)
        self._source = trace
        self._name_dict = trace._name_dict
        self._reverse_name_dict = trace._reverse_name_dict

    def global_events(self):
        return filter(self._filter, self._source.global_events())

    def device_events(self, device_id):
        return filter(self._filter, self._source.device_events(device_id))

    def devices(self):
        return self._source.devices()


class NameBasedFilterer(TraceFilterer):
    def __init__(self, trace: Trace, names, disallowed=False) -> None:
        super().__init__(trace)
        self._names = set(names)
        self._filter = self._filter_disallowed if disallowed else self._filter_allowed

    def _filter_allowed(self, event: Event):
        return event.name in self._names

    def _filter_disallowed(self, event: Event):
        return event.name not in self._names

class DurationBasedFilterer(TraceFilterer):
    def __init__(self, trace: Trace, durations) -> None:
        super().__init__(trace)
        
        ureg = pint.UnitRegistry()

        # Durations is a list of tuples: (event_name,min_duration,max_duration) e.g. (device_inference,5us,10ms)
        # To allow any [min|max]_duration, simply add a "*" in, e.g. (device_inference,*,10ms)
        # We allow all names which aren't mentioned
        self._durations = {}
        for name, min_dur, max_dur in durations:
            if name in self._durations:
                raise ValueError(f"Event name: {name} mentioned twice in durations list")

            if min_dur == "*":
                min_dur = "-1ns"
            if max_dur == "*":
                max_dur = f"{MAX_INT_64}ns"

            min_dur_ns = ureg(min_dur).to(ureg.ns).m
            max_dur_ns = ureg(max_dur).to(ureg.ns).m
            self._durations[name] = (min_dur_ns, max_dur_ns)
    
    def _filter(self, event: Event):
        if event.name not in self._durations:
            return True
        min_dur, max_dur = self._durations[event.name]
        dur = event.end_ns - event.start_ns
        return min_dur < dur and dur < max_dur

@enable_chaining
def load_trace(abs_trace_path: str = "", __entry__=None):
    return TraceReader(abs_trace_path, __entry__)

@enable_chaining
def allow_names(trace_obj: Trace = None, allowed_names=[]):
    return NameBasedFilterer(trace_obj, allowed_names)


@enable_chaining
def disallow_names(trace_obj: Trace = None, disallowed_names=[]):
    return NameBasedFilterer(trace_obj, disallowed_names, disallowed=True)

@enable_chaining
def filter_using_durations(trace_obj: Trace = None, durations=[]):
    return DurationBasedFilterer(trace_obj, durations)

@enable_chaining
def count(trace_obj=None, per_device=False):
    event_counter = Counter()

    for ev in trace_obj.global_events():
        event_counter.update([ev.name])

    if per_device:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                name = f"{ev.name}_device={device_id}"
                event_counter.update([name])
    else:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                event_counter.update([ev.name])

    for event_name, count in event_counter.items():
        print(f"{event_name: <30} {count}")


@enable_chaining
def show(trace_obj=None):
    events = [copy.deepcopy(e) for e in trace_obj.global_events()]

    for device_id in trace_obj.devices():
        events += [copy.deepcopy(e) for e in trace_obj.device_events(device_id)]

    events.sort(key=lambda e: e.start_ns)
    for event in events:
        print(event, (event.end_ns - event.start_ns) * 1e-6)


@enable_chaining
def summarise(trace_obj=None, per_device=False, __entry__=None):
    events = {}

    for ev in trace_obj.global_events():
        if ev.is_counter_event:
            continue
        duration = ev.end_ns - ev.start_ns
        events.setdefault(ev.name, []).append(duration)

    if per_device:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                if ev.is_counter_event:
                    continue
                name = f"{ev.name}_device={device_id}"
                duration = ev.end_ns - ev.start_ns
                events.setdefault(name, []).append(duration)
    else:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                if ev.is_counter_event:
                    continue
                duration = ev.end_ns - ev.start_ns
                events.setdefault(ev.name, []).append(duration)
    
    table = []
    summary_dict = {}
    for name, durations in events.items():
        mean = np.mean(durations)
        stddev = np.std(durations)
        p99 = np.percentile(durations, 99)
        _max = np.max(durations)

        formatted_mean_stddev = f"{mean * 1e-6: >10.3f}ms ± {stddev * 1e-6: >5.3f}"
        formatted_p99 = f"{p99 * 1e-6: >10.3f}ms"
        formatted_max = f"{_max * 1e-6: >10.3f}ms"

        table.append([name, formatted_mean_stddev, formatted_p99, formatted_max])

        summary_dict[name] = {
            "mean_ms": "{:.3f}".format(mean * 1e-6),
            "stddev_ms": "{:.3f}".format(stddev * 1e-6),
            "p99_ms": "{:.3f}".format(p99 * 1e-6),
            "max_ms": "{:.3f}".format(_max * 1e-6)
        }

    print(tabulate.tabulate(table, headers=["Event Name", "Mean ± Stddev", "p99", "Max"], tablefmt="github"))

    trace_obj.__entry__.plant("trace_summary", summary_dict)
    trace_obj.__entry__.save()

@enable_chaining
def summarise_counters(trace_obj=None, per_device=True):
    events = {}

    for ev in trace_obj.global_events():
        if not ev.is_counter_event:
            continue
        events.setdefault(ev.name, []).append(ev.counter_value)

    if per_device:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                if not ev.is_counter_event:
                    continue
                name = f"{ev.name}_device={device_id}"
                events.setdefault(name, []).append(ev.counter_value)
    else:
        for device_id in trace_obj.devices():
            for ev in trace_obj.device_events(device_id):
                if not ev.is_counter_event:
                    continue
                events.setdefault(ev.name, []).append(ev.counter_value)
    
    table = []
    for name, values in events.items():
        mean = np.mean(values)
        stddev = np.std(values)
        _max = np.max(values)
        _min = np.min(values)

        formatted_mean_stddev = f"{mean : >10.3f} ± {stddev : >5.3f}"
        formatted_max = f"{_max : >10.3f}"
        formatted_min = f"{_min : >10.3f}"

        table.append([name, formatted_mean_stddev, formatted_max, formatted_min])

    print(tabulate.tabulate(table, headers=["Event Name", "Mean ± Stddev", "Max", "Min"], tablefmt="github"))

@enable_chaining
def get_counter_frequencies(trace_obj=None, counter_name=""):
    trace_obj = NameBasedFilterer(trace_obj, [counter_name])
    
    freqs = Counter()
    for ev in trace_obj.global_events():
        if not ev.is_counter_event:
            continue
        freqs.update([ev.counter_value])
    
    for device_id in trace_obj.devices():
        for ev in trace_obj.device_events(device_id):
            if not ev.is_counter_event:
                continue
            freqs.update([ev.counter_value])
    
    for k, freq in sorted(freqs.items()):
        print(f"{k}: {freq}")
