# warmup_project
Written by Matthias Ling

## Drive Square 
### Description
I had the robot drive in a straight line for a certain amount of time (4 or 5 seconds) before turning 90 degrees counterclockwise.  I then looped this 4 times.  I wanted to do it based on time because I thought it was the most straightforward.  
### Code explanation
The drive function just ran the loop.  Besides that, I had two functions: run (for driving straight) and rotate (for rotating).  Run sets the linear.x of the twist and sleeps for 4 or 5 seconds.  Rotate does the same but for the angular.z and sets it to pi/2 / (sleep time).  This allows me to calculate extactly 90 degrees, because the speed * sleep time will result in a pi/2 angular transformation
### Gif
![](drive_square.mp4)

## Person Follower
### Description
My person follower just sets a standard linear speed unless it's too close to the person.  It then also sets an angular speed depending on which side (left or right) of the robot the person is standing on.
### Code explanation
I had the overall drive function again, as well as a scan function.  This scan function would just check if the person was within the minimum threshold.  If they were, it would negate linear.x.  If not, it would set it to a predetermined value and would calculate which side of the robot the person was on (looking at data.ranges).  It would adjust the angular velocity to positive or negative depending on the side.  Thus, the robot is constantly adjusting.
### Gif
![](person_follower.mp4)

## Wall Follower
### Description
### Code explanation
### Gif