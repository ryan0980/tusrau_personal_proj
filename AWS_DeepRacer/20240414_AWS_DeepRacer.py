def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    is_crashed = params['is_crashed']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    steps = params['steps']
    progress = params['progress']

    # 如果车辆不在赛道上或已经碰撞，则返回最小奖励
    if not all_wheels_on_track or params['is_reversed'] or params['is_offtrack'] or params['is_crashed']:
        return 1e-3

    reward = 5.0  # 初始奖励

    # 根据车辆距离赛道中心的远近调整奖励
    outer_radius = track_width*0.8
    mid_radius = track_width*0.5
    inner_radius = track_width*0.25

    if distance_from_center <= inner_radius:
        reward += 1.0
        reward += 1.5 if speed > 3 else 0.9
    elif distance_from_center <= mid_radius:
        reward += 0.7
        reward += 1.3 if speed > 3 else 0.7
    elif distance_from_center <= outer_radius:
        reward += 0.4
        reward += 1.0 if speed > 3 else 0.5

    # 考虑车辆的转向角度和速度的组合
    ABS_STEERING_THRESHOLD = 18.0
    if abs(steering_angle) > ABS_STEERING_THRESHOLD:
        if speed > 1.5:
            reward += 0.8
        else:
            reward -= 0.5  # 转弯时速度太慢则惩罚
    if speed > 3:
        reward += 2.0
    elif speed > 2:
        reward += 1.0
    elif speed > 1:
        reward += 0.5

    # 可以根据需要启用以下注释掉的代码段
    '''
    if -10 < steering_angle < 10:
        if speed > 2:
            reward += 2.0
        else:
            reward += 1.2
    elif -20 > steering_angle or 20 < steering_angle:
        if speed > 2:
            reward += 1.0
        else:
            reward += 1.1
    else:
        if speed > 2:
            reward += 0.6
        else:
            reward += 0.4
    '''

    # 基于进度和步数的效率奖励
    if steps > 0 and progress > 0:
        efficiency = progress / steps
        reward += efficiency * 5.0

    return float(reward)
