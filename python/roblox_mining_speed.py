from itertools import product
import pandas as pd

# Constants and given values
base_hit = 31
num_of_triggers = 3
ss_total_time = 187

# Define the ranges for each gadget type based on constraints
ss_range = range(0, 2)  # 0 to 1
mg_range = range(0, 4)  # 0 to 3
bhg_range = range(0, 3)  # 0 to 2
hg_range = range(0, 2)  # 0 to 1
shg_range = range(0, 3)  # 0 to 2

# Store all valid combinations and their computed results
results = []

# Iterate over all possible values using nested loops
for x_ss, x_mg, x_hg, x_shg, x_bhg in product(ss_range, mg_range, hg_range, shg_range, bhg_range):
    if x_ss + x_mg + x_hg + x_shg + x_bhg == 6:
        # Calculate swings_per_sec
        swings_per_sec = 2 * (sum(1.13 for _ in range(x_hg + 1)) + sum(1.21 for _ in range(x_shg + 1)) + sum(1.10 for _ in range(x_bhg + 1)))

        # Calculate prob_double, capped at a maximum of 1
        prob_double = min(0.4 * x_mg, 1)

        # Calculate blocks_per_hit
        blocks_per_hit = (base_hit * (2 * prob_double)) + (base_hit * (1 - prob_double))

        # Calculate ss_mode_time and prob_ss
        ss_mode_time = num_of_triggers * 15  # 15 seconds per trigger

        # Calculate the final result based on the value of x_ss
        if x_ss == 0:
            result = swings_per_sec * blocks_per_hit
            prob_ss = 0
        else:
            prob_ss = ss_mode_time / ss_total_time
            result = swings_per_sec * blocks_per_hit * (2 * prob_ss + (1 - prob_ss))

        # Store the results
        results.append((x_ss, x_mg, x_hg, x_shg, x_bhg, swings_per_sec, blocks_per_hit, prob_double, prob_ss, result))

# Convert the results into a DataFrame for visualization
columns = ["SS", "MG", "HG", "SHG", "BHG", "Swings/sec", "Blocks/Hit", "Prob Double", "Prob SS", "Result"]
results_df = pd.DataFrame(results, columns=columns)
print(results_df.sort_values(by='Result', ascending=False))

max_result_index = results_df['Result'].idxmax()

# Display the entire row with the highest result
row_with_highest_result = results_df.loc[max_result_index]

print(row_with_highest_result)

print("")
print(f"{(row_with_highest_result['Result'] * 60 * 60 * 8)/1_000_000} ab in 8 hrs")
