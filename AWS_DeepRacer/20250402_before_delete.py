def reward_function(params):
    #############################################################################


    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    closest_objects = params['closest_objects']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    is_crashed = params['is_crashed']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    heading = params['heading']
    objects_distance = params['objects_distance']
    objects_heading = params['objects_heading']
    objects_left_of_center = params['objects_left_of_center']
    objects_location = params['objects_location']
    objects_speed = params['objects_speed']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_length = params['track_length']
    track_width = params['track_width']
    waypoints = params['waypoints']

    

    if not all_wheels_on_track:
        reward = 1e-3
        return float(reward)#return 1e-3 if all_wheels_on_track is False
    
    reward = 1.0#init reward

    outer_radius = track_width*0.8
    mid_radius = track_width*0.6
    inner_radius = track_width*0.35

    if distance_from_center <= inner_radius:
        reward += 2.0  # Closest to the center gets the highest reward
    elif distance_from_center <= mid_radius:
        reward += 1.3  # Middle tier distance gets a medium reward
    elif distance_from_center <= outer_radius:
        reward += 0.5  # Outer tier distance gets a lower reward
    
    if -10 < steering_angle < 10:
        reward += 1.0 if speed > 2 else 0.5
    elif abs(steering_angle) > 20:
        reward += 0.7 if speed > 2 else 1.3
    else:
        reward += 0.4 if speed > 2 else 0.8



    if steps > 0:
        progress_ratio = progress / 100
        efficiency = progress_ratio / steps
        step_reward = efficiency * 500  # 增加效率系数
        reward += step_reward
        reward *= (1.0 + 0.5 / steps)
    

    return float(reward)
            
