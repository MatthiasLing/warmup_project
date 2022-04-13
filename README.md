# warmup_project
Written by Matthias Ling

## Drive Square 
### Description
I had the robot drive in a straight line for a certain amount of time (4 or 5 seconds) before turning 90 degrees counterclockwise.  I then looped this 4 times.  I wanted to do it based on time because I thought it was the most straightforward.  
### Code explanation
The drive function just ran the loop.  Besides that, I had two functions: run (for driving straight) and rotate (for rotating).  Run sets the linear.x of the twist and sleeps for 5 seconds.  Rotate does the same but for the angular.z and sets it to pi/2 / (sleep time).  This allows me to calculate extactly 90 degrees, because the speed * sleep time will result in a pi/2 angular transformation.  I had to subtract a small amount of time for the rest during rotate to account for angular acceleration.
### Gif
![](drive_square.gif)

## Person Follower
### Description
My person follower just sets a standard linear speed unless it's too close to the person.  It then also sets an angular speed depending on which side (left or right) of the robot the person is standing on.
### Code explanation
I had the overall drive function again, as well as a scan function.  This scan function would just check if the person was within the minimum threshold.  If they were, it would negate linear.x.  If not, it would set it to a predetermined value and would calculate which side of the robot the person was on (looking at data.ranges).  It would adjust the angular velocity to positive or negative depending on the side.  Thus, the robot is constantly adjusting.  If the person's behind the robot (angle in range(90,270)), it'll only turn and not move forward.  I conclude the function by publishing the twist.
### Gif
![](person_follower.gif)

## Wall Follower
### Description
I used the approach of finding the wall first and then navigating from there.  Similarly to person_follower, I would adjust the rotational velocity and move forward constantly until the nearest wall was the minimum distance from the robot.  Then, I would direct the bot to turn proportionally depending on the difference from the angle of the closest point and 90 degrees.  This would allow it to stay a constant distance from the wall.
### Code explanation
All the maneuvering is done in the scan function.  First, I navigate to the wall if the robot is too far away.  Otherwise, I normalize the angle of the nearest point to 270 degrees (270->90 degrees is 0->180 degrees and the rest is 0->-180 degrees).  This makes it easy to enact proportional control for the robot's angular velocity.  I define a standard kp value, and multiply kp*(normalized angle) / (some arbitrary constant).  I conclude the function by publishing.
### Gif
![](wall_follower.gif)

## Challenges
My biggest challenge of this project by far was trying to get the linux machine set up.  I ended up deleting Virtual Box and using UTM the night before the due date.  I also faced some challenges implementing proportional control with the robot.  This was solved largely through trial and error, playing around with the kp/constant values until the robot ran smoothly.  
## Future Work
I would try to make the wall follower code run smoother for edge cases and have more fluid rotations. Right now it's a bit jerky.  I would also adjust the robot's linear speed proportionally in the person follower, because it makes the robot move organically without risking it moving too far away from the original target.
## Takeaways
* Technical debt - take more time to pick the best tool to use.  For me installing UTM on Monday night was clutch, but I still wasted a lot of time trying to use virtual box.
* Understand robot behavior in terms of principles, not individual cases - this was helpful for the last two parts.  I think that the general application of rules - adjusting rotational velocity according to simpler demarcations made the code easier and simpler than trying to manually partition the angles into separate cases and trying to operate on them separately.  This was a less intuitive perspective on the robot's behaviors and probably overcomplicated the whole thing.