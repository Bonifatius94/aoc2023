from typing import List, Union, Tuple, Dict, Any

FLIP_FLOP = "%"
CONJUNCTION = "&"
BROADCAST = "broadcaster"
ConnType = Any # Union[FLIP_FLOP, CONJUNCTION, BROADCAST]

HIGH = "high"
LOW = "low"
Pulse = Union[HIGH, LOW]
Signal = Tuple[str, str, Pulse]

Edges = Dict[str, List[str]]
Connection = Tuple[str, ConnType]
FlipFlopState = bool
ConjState = Dict[str, Pulse]
ConnState = Union[FlipFlopState, ConjState, None]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def group_by(values: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    res: Dict[Any, List[Any]] = dict()
    for k, v in values:
        if k in res:
            res[k].append(v)
        else:
            res[k] = [v]
    return res


def process_signal(
        conn_type: ConnType, signal: Signal,
        outgoing: List[str], state: ConnState
    ) -> Tuple[ConnState, List[Signal]]:
    sender, receiver, pulse = signal
    if conn_type == FLIP_FLOP:
        if pulse == HIGH:
            return state, []
        else:
            out_pulse = LOW if state else HIGH
            return not state, [(receiver, n, out_pulse) for n in outgoing]
    elif conn_type == CONJUNCTION:
        state[sender] = pulse
        all_high = all([state[pred] == HIGH for pred in state])
        out_pulse = LOW if all_high else HIGH
        return state, [(receiver, n, out_pulse) for n in outgoing]
    elif conn_type == BROADCAST:
        return None, [(receiver, n, LOW) for n in outgoing]
    return state, []


def simulate_signals(
        nodes: List[Tuple[str, ConnType, List[str]]],
        init_signal: Signal, steps: int) -> int:
    low_pulses, high_pulses = 0, 0
    edges = [(n1, n2) for n1, _, out in nodes for n2 in out]
    incoming, outgoing = group_by([(n2, n1) for n1, n2 in edges]), group_by(edges)
    conn_types = dict([(n, t) for n, t, _ in nodes])

    def init_state(conn_name: str, conn_type: ConnType) -> ConnState:
        if conn_type == CONJUNCTION:
            return dict([(n, LOW) for n in incoming[conn_name]])
        elif conn_type == FLIP_FLOP:
            return False
        else:
            return None

    conn_states = dict([(n, init_state(n, t)) for n, t, _ in nodes])

    for _ in range(steps):
        signals = [init_signal]
        while signals:
            signal = signals.pop(0)
            sender, receiver, pulse = signal
            # print(f"{sender} -{pulse}-> {receiver}")
            if pulse == LOW:
                low_pulses += 1
            elif pulse == HIGH:
                high_pulses += 1

            if receiver not in outgoing:
                continue

            conn_type, conn_state = conn_types[receiver], conn_states[receiver]
            state, new_signals = process_signal(
                conn_type, signal, outgoing[receiver], conn_state)
            conn_states[receiver] = state
            for s in new_signals:
                signals.append(s)

    return low_pulses * high_pulses


def main():
    lines = read_lines()
    nodes = [(line[1:line.index("->")-1], line[0], line[line.index("->")+2:].strip().split(", "))
             for line in lines if line[0] in [FLIP_FLOP, CONJUNCTION]]
    broadcast = [(BROADCAST, BROADCAST, line[line.index("->")+2:].strip().split(", "))
                 for line in lines if line.startswith(BROADCAST)]
    nodes = nodes + broadcast

    initial_signal = ("button", BROADCAST, LOW)
    pulse_count = simulate_signals(nodes, initial_signal, 1_000)
    print("pulse count is", pulse_count)


if __name__ == "__main__":
    main()
