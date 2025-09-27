@report LAB:
  typst compile ./{{LAB}}/report/report.typ --root {{LAB}}

@watch LAB:
  typst watch ./{{LAB}}/report/report.typ --root {{LAB}}

@open LAB:
  @just report {{LAB}}
  start ./{{LAB}}/report/report.pdf

