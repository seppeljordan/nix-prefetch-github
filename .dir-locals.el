((org-mode . ((org-confirm-babel-evaluate
               .
               (lambda (lang body)
                 (not (string= lang "sh")))))))
