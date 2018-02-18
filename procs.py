import math

import functions as fn

def smooth_white(state):
    offset = (state.v / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    w = 0.1

    return (r, r, r, r)


def const_step(state):
    i = 11
    if state.v == i:
        return (1.0, 0, 0, 1)
    if state.v == i + 1:
        return (0, 1, 1, 0)
    return (0,0,0,0)



def const_colors(state):
    c = [(0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0)]

    return c[state.v % 4]


def smooth_colors(state):
    offset = (state.v / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * state.t + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * state.t + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * state.t + 4 + offset)
    w = 0.1

    return (r, g, b, w)



def color_flow(state):

    p_r = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t))
    p_g = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t + 1.0))
    p_b = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t + 2.0))

    r = 0.0
    g = 0.0
    b = 0.0

    if abs(state.v - p_r) < 0.5:
        r = 1.0

    if abs(state.v - p_g) < 0.5:
        g = 1.0

    if abs(state.v - p_b) < 0.5:
        b = 1.0

    return (r, g, b, 0.1)




def flow_pulse(state):
    pulse_len = 4.5

    blue_base = 0.2

    # hull parabola / outer fade
    f_hull = fn.linear_window(-2, state.v_res + 1, state.v)
    hull = fn.mix(0.1, 1.0, fn.parabola(8, f_hull))

    # flowing pulse
    v_pos = fn.linear_window_duration(1, pulse_len, state.t % (pulse_len * 1.5)) * (state.v_res + 8)
    f_pulse = fn.linear_window(-8 + v_pos, 0 + v_pos, state.v)
    pulse = fn.parabola(4, f_pulse) * hull

    # flowing pulse
    v_pos2 = fn.linear_window_duration(1.4, pulse_len, state.t % (pulse_len * 1.5)) * (state.v_res + 8)
    f_pulse2 = fn.linear_window(-8 + v_pos2, 0 + v_pos2, state.v)
    pulse2 = fn.parabola(4, f_pulse2) * hull

    return (0, pulse2, blue_base, pulse)


def pulse_wob(state):
    blue_base = 0.2

    pulse_base = 1.0 - fn.impulse(8,
                                  fn.linear_window_duration(
                                    4, 1, state.t % 10.0))


    pulse_up = fn.impulse(8, fn.linear_window(pulse_base * state.v_res - 1,
                                               pulse_base * state.v_res + 8,
                                               state.v))

    return (0, 0, blue_base, pulse_up * 0.7)


def random_glow(state):
    randomize = [(9, 2, 4, 8), (0, 2, 5), (3, 10, 12), (0, 3, 5, 12),
                 (4, 9), (2, 9, 11), (4, 8), (1, 5, 10, 12, 7),
                 (1,), (3, 8, 12), (9,), (2, 10, 0), (4, 11, 5, 7),
                 (0, 2, 5, 8, 12), (0, 4), (9, 12), (1, 3, 6),
                 (0, 4, 7), (9, 3, 12), (0, 5, 12)]

    duration = 1

    glow_fn = fn.impulse

    total_win_size = len(randomize) * duration

    select = math.floor((state.t % total_win_size) / duration)
    selected = randomize[select]

    pulse_t = fn.mix(0, 1, state.t % duration)

    if state.v in selected:
        pulse = fn.impulse(12, pulse_t)
        return (0, 0, 0, pulse)

    return (0,0,0,0)


def random_color_glow(state):
    colors = smooth_colors(state)
    glows = random_glow(state)

    return (0.5 * colors[0], 0.5 * colors[1], 0.5* colors[2], glows[3])


