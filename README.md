# milb_tiebreaker
Tie-Breaking Procdure for a Minor League Baseball League

I don't follow minor league baseball, but I ended up with some free tickets to our local team, the Columbus Clippers in the spring of 2022. Out of curiosity, I checked the standings to see how their season was going. They were just a few games out of first place. The website for the league had a description of the tie-breaking procedure in case one or more teams were tied for first place at the end of the season, as only one can advance to the playoffs. The description of the procedure seemed interesting and just complex enough to make me wonder how they managed to figure it out. It seemed like a perfect problem to solve with computer programs.

The procedure is as follows: if multiple teams are tied, whoever has the best record in head-to-head games among the tied teams (it can be 2 or more) is the winner. If this doesn't break the tie, then the team with the best record in the last 20 games of the season wins. If the records are the same it goes on to 21 games, 22, and so on until the tie is broken.

The fact that it's an open-ended problem added to the interest. I used this as an opportunity to start working with the pandas module in Python. I used pandas to store a short season of simulated games as a data frame and sorted and filtered the data frame to determine winning percentages of all the teams. 

My favorite part of this exercise was the successful utilization of a recursive function. I didn't set out to do this or incorporate the recursive function just for the sake of doing it; as I worked on the issue of how to solve the issue of checking the past 20 games, and then adding one game and checking again until the tie was broken, it just occurred to me as a natural solution. This helped me learn an important principle: it's hard to truly understand a coding technique until one actually uses it in practice. I had read about recursion before and understood it in a superficial, "I can recite the words," kind of way until I actually used recursion and in doing so gained a real understanding of when and how it's used in solving real world problems.

