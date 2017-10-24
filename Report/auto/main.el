(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "10pt" "twoside")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("xcolor" "table" "xcdraw") ("algorithm" "Alg.")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "inputenc"
    "natbib"
    "graphicx"
    "booktabs"
    "amsmath"
    "amsfonts"
    "adjustbox"
    "xcolor"
    "todonotes"
    "fancyhdr"
    "multirow"
    "algorithm"
    "algpseudocode"
    "anysize")
   (TeX-add-symbols
    '("ignore" 1))
   (LaTeX-add-labels
    "sec_intro"
    "sec_SoA"
    "sec_mathmod"
    "sec_results"
    "sec_sol"
    "sec_eval"
    "sec_conclusions")
   (LaTeX-add-bibliographies
    "bibliografia"))
 :latex)

