@setup:
  uv sync

@report LAB:
  typst compile ./src/{{LAB}}/report/report.typ --root .

@watch LAB:
  typst watch ./src/{{LAB}}/report/report.typ --root .

@open LAB:
  @just report {{LAB}}
  start ./src/{{LAB}}/report/report.pdf

@archive:
  @just report lab1
  git archive -o labs.zip HEAD