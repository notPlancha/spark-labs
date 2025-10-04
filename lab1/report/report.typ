#import "@preview/callisto:0.2.4"
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.8": *
#show: codly-init.with()
#codly(
  languages: (
    // python: (name: [#h(-0.3em)], icon: codly-languages.python.icon),
    python: codly-languages.python,
    txt: (name: "out")
  ),
)

#show heading.where(level: 1): set text(size: 40pt)

= Starting the Cluster

```sh

```

#pagebreak()

= Task 1

#callisto.render(nb: json("/lab1/task1.ipynb"))

#pagebreak()

= Task 2
#callisto.render(nb: json("/lab1/task2.ipynb"))
