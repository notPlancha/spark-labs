#import "@preview/callisto:0.2.4"

#show heading.where(level: 1): set text(size: 40pt)

= Task 1

#callisto.render(nb: json("/task1.ipynb"))

#pagebreak()

= Task 2
#callisto.render(nb: json("/task2.ipynb"))
