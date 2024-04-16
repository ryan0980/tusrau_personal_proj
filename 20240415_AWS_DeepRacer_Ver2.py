import math

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_curve(pointA, pointB, pointC):
    a = calculate_distance(pointB, pointC)
    b = calculate_distance(pointA, pointC)
    c = calculate_distance(pointA, pointB)
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    if area == 0:
        return 0
    R = (a * b * c) / (4 * area)
    return 1 / R

def calculate_direction_diff(track_direction, heading):
    direction_diff = abs(track_direction - heading)
    return 360 - direction_diff if direction_diff > 180 else direction_diff

def get_optimal_speed(curve, high_curve=60, low_speed=0.8, high_speed=1.5):
    return low_speed if curve > high_curve else high_speed

def reward_function(params):
    reward = 1
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # 基础惩罚
    if not all_wheels_on_track or params['is_reversed'] or params['is_offtrack'] or params['is_crashed']:
        return 1e-3

    # 奖励距离中心线的距离
    distance_rewards = [1.0, 0.5, 0.1, 1e-3]
    markers = [track_width / 8.0, track_width / 4.0, track_width / 2.0, track_width]
    reward += next((r for d, r in zip(markers, distance_rewards) if distance_from_center <= d), 0)
    SPEED_THRESHOLD = 1.5
    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward += 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward += 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward += 1.0


    # 方向控制
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))
    direction_diff = calculate_direction_diff(track_direction, heading)
    DIRECTION_THRESHOLD = 10.0
    reward *= 0.5 if direction_diff > DIRECTION_THRESHOLD else 1

    # 曲率与速度管理
    current_position = (params['x'], params['y'])
    next_waypoint_index = closest_waypoints[1]
    next_waypoint = waypoints[next_waypoint_index]

    def calculate_heading_change(current_heading, next_waypoint, current_position):
        dx = next_waypoint[0] - current_position[0]
        dy = next_waypoint[1] - current_position[1]
        desired_heading = math.degrees(math.atan2(dy, dx))
        angle_change = desired_heading - current_heading
        # Normalize to -180 to 180
        angle_change = (angle_change + 180) % 360 - 180
        return angle_change

    def is_next_turn_left(current_heading, next_waypoint, current_position):
        angle_change = calculate_heading_change(current_heading, next_waypoint, current_position)
        return angle_change < 0  # Negative angle change indicates a left turn

    next_turn_is_left = is_next_turn_left(heading, next_waypoint, current_position)

    if next_turn_is_left:
        if not is_left_of_center:
            reward += 1.0  # Reward being on the right if the next turn is left
        else:
            reward += 0.5  # Lesser reward for not being optimally positioned
    else:
        if is_left_of_center:
            reward += 1.0  # Reward being on the left if the next turn is right
        else:
            reward += 0.5  # Lesser reward for not being optimally positioned

    # 曲率与速度管理
    prev_wp, next_wp = closest_waypoints
    pointC = waypoints[next_wp + 1] if next_wp + 1 < len(waypoints) else waypoints[0]
    curve = calculate_curve(waypoints[prev_wp], waypoints[next_wp], pointC)
    optimal_speed = get_optimal_speed(curve)
    reward += speed / optimal_speed

    # 细化奖励计算并规范化奖励
    reward = max(min(reward, 1.0), 0.0)
    return float(reward)