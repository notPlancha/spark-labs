@report LAB:
  typst compile ./{{LAB}}/report/report.typ --root .

@watch LAB:
  typst watch ./{{LAB}}/report/report.typ --root .

@open LAB:
  @just report {{LAB}}
  start ./{{LAB}}/report/report.pdf
