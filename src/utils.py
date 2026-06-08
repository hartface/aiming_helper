import bpy
from mathutils import Vector
import math
import gpu
import blf
from gpu_extras.batch import batch_for_shader


def get_world_positions(props):

    points = []
    pairs = [
        (props.eye_set,         props.eye_object,         props.eye_local_pos),
        (props.rear_sight_set,  props.rear_sight_object,  props.rear_sight_local_pos),
        (props.front_sight_set, props.front_sight_object, props.front_sight_local_pos),
        (props.target_set,      props.target_object,      props.target_local_pos),
    ]

    for is_set, obj, local_pos in pairs:
        if is_set and obj:
            world_pos = obj.matrix_world @ Vector(local_pos)
            points.append(world_pos)
    return points


def get_max_deviation(points):

    if len(points) < 3:
        return 0.0

    start = points[0]
    end = points[-1]
    line = end - start
    line_len = line.length
    if line_len == 0:
        return 0.0

    max_dev = 0.0
    for p in points[1:-1]:
        to_p = p - start
        proj = to_p.project(line)
        deviation = (to_p - proj).length

        if deviation > max_dev:
            max_dev = deviation

    return max_dev


def get_angle_deg(a, b, c):
    v1 = (a - b).normalized()
    v2 = (c - b).normalized()
    dot = max(-1.0, min(1.0, v1.dot(v2)))
    return math.degrees(math.acos(dot))


def deviation_to_color(deviation, threshold):
    t = min(deviation / (threshold * 4), 1.0)
    if t < 0.5:
        return (t * 2.0, 1.0, 0.0, 1.0)
    else:
        return (1.0, 1.0 - (t - 0.5) * 2.0, 0.0, 1.0)


def draw_callback_3d(self, context):
    props = context.scene.aiming_helper
    if not props.visualizing:
        return

    points = get_world_positions(props)
    if len(points) < 2:
        return

    deviation  = get_max_deviation(points)
    line_color = deviation_to_color(deviation, props.threshold)

    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    gpu.state.blend_set('ALPHA')

    gpu.state.line_width_set(2.5)
    batch_line = batch_for_shader(shader, 'LINE_STRIP', {"pos": points})
    shader.bind()
    shader.uniform_float("color", line_color)
    batch_line.draw(shader)

    if len(points) >= 3:
        start = points[0]
        end   = points[-1]
        line  = end - start
        gpu.state.line_width_set(1.0)
        for p in points[1:-1]:
            to_p        = p - start
            proj_vec    = to_p.project(line)
            ideal_point = start + proj_vec
            batch_dev   = batch_for_shader(shader, 'LINES', {"pos": [p, ideal_point]})
            shader.uniform_float("color", (1.0, 1.0, 1.0, 0.3))
            batch_dev.draw(shader)

    gpu.state.point_size_set(10.0)
    batch_dots = batch_for_shader(shader, 'POINTS', {"pos": points})
    shader.uniform_float("color", (1.0, 1.0, 1.0, 1.0))
    batch_dots.draw(shader)

    gpu.state.blend_set('NONE')


def draw_callback_2d(self, context):
    props = context.scene.aiming_helper
    if not props.visualizing:
        return

    points = get_world_positions(props)
    region = context.region
    rv3d   = context.region_data
    font_id = 0

    deviation  = get_max_deviation(points)
    line_color = deviation_to_color(deviation, props.threshold)

    from bpy_extras.view3d_utils import location_3d_to_region_2d

    # Labels and angles at each point
    labels = ['Eye', 'Rear', 'Front', 'Target']
    for i, (p, label) in enumerate(zip(points, labels)):
        screen_pos = location_3d_to_region_2d(region, rv3d, p)
        if screen_pos is None:
            continue

        blf.size(font_id, 13)
        blf.color(font_id, *line_color[:3], 1.0)
        blf.position(font_id, screen_pos.x + 10, screen_pos.y + 10, 0)
        blf.draw(font_id, label)

        if 0 < i < len(points) - 1:
            angle = get_angle_deg(points[i - 1], p, points[i + 1])
            blf.size(font_id, 11)
            blf.color(font_id, 1.0, 1.0, 1.0, 0.8)
            blf.position(font_id, screen_pos.x + 10, screen_pos.y - 8, 0)
            blf.draw(font_id, f"{angle:.1f}°")

    blf.size(font_id, 14)
    if len(points) >= 2:
        if deviation <= props.threshold:
            blf.color(font_id, 0.0, 1.0, 0.2, 1.0)
            blf.position(font_id, 20, 80, 0)
            blf.draw(font_id, "Aligned")
        else:
            blf.color(font_id, 1.0, 0.3, 0.3, 1.0)
            blf.position(font_id, 20, 80, 0)
            blf.draw(font_id, f"Misaligned  ({deviation:.3f}m off)")

    total_set = sum([
        props.eye_set, props.rear_sight_set,
        props.front_sight_set, props.target_set
    ])
    if total_set < 4:
        blf.size(font_id, 12)
        blf.color(font_id, 0.7, 0.7, 0.7, 0.8)
        blf.position(font_id, 20, 60, 0)
        blf.draw(font_id, f"{total_set}/4 points set")
