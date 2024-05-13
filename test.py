nums = [2,7,11,15]
target = 9
seen = {}
for i, value in enumerate(nums):
   remaining = target - nums[i]

   if remaining in seen:
       print([i, seen[remaining]])
    
   seen[value] = i