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
    if not all_wheels_on_track or is_crashed:
        reward = 1e-3
        return float(reward)

    reward = 5.0  # 初始奖励

    # 根据车辆距离赛道中心的远近调整奖励
    outer_radius = track_width / 2.0
    mid_radius = track_width / 4.0
    inner_radius = track_width / 8.0

    if distance_from_center <= inner_radius:
        reward += 1.0
        reward += 2.0 if speed > 3 else 0.9
    elif distance_from_center <= mid_radius:
        reward += 0.7
        reward += 1.5 if speed > 3 else 0.6
    elif distance_from_center <= outer_radius:
        reward += 0.4
        reward += 1.0 if speed > 3 else 0.3

    # 考虑车辆的转向角度和速度的组合
    if abs(steering_angle) > 20:
        if speed > 3:
            reward -= 1.0  # 在大角度转向时高速行驶，大幅度减少奖励
        else:
            reward += 1.5  # 在大角度转向时低速行驶，适当增加奖励
    else:
        if speed > 3.5:
            reward += 4.0  # 最高速度区间，给予最高奖励
        elif speed > 3.0:
            reward += 2.5
        elif speed > 2.5:
            reward += 1.8
        elif speed > 2.0:
            reward += 1.3
        else:
            reward += 0.1

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
    if steps > 0:
        progress_ratio = progress / 100
        efficiency = progress_ratio / steps
        step_reward = efficiency * 40
        reward += step_reward

    return float(reward)
