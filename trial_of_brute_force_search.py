import numpy as np


def brute_force_search(frame):
    
    best_radius = 0
    best_mid_x = 0
    best_mid_y = 0
    
    best_score = 0
    
    x_len = frame.shape[1]
    y_len = frame.shape[0]
    
    for mid_x in range(int((1/3)*x_len), int((2/3)*x_len)):
        
        for mid_y in range((int(1/3)*y_len), int((2/3)*y_len)):
            
            for radius in range(int((1/3)*x_len), int((2/3)*x_len)):
                
                score = try_diff_frame_values(frame, mid_x, mid_y, radius)
                
                if score > best_score:
                    best_score = score
                    best_radius = radius
                    best_mid_x = mid_x
                    best_mid_y = mid_y
    
    return best_radius, best_mid_x, best_mid_y


def try_diff_frame_values(frame, mid_x, mid_y, radius):
    
    white_vals_x = np.where(frame > 5)[0]
    white_vals_y = np.where(frame > 5)[1]
    
    score = 0

    for white_val in range(len(white_vals_x)):

        x_val = white_vals_x[white_val]
        y_val = white_vals_y[white_val]
        
        funct_val = np.sqrt(radius **2 - (x_val - mid_x)**2) + mid_y
        
        if funct_val == y_val:
            score += 1
    
    print(score)
    return score
