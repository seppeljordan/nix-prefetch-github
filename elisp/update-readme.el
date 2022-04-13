(progn
  (setq org-confirm-babel-evaluate
	(lambda (lang body) (not (string= lang "sh"))))
  (org-babel-do-load-languages
   'org-babel-load-languages
   '((shell . t)))
  (org-babel-execute-buffer)
  (save-buffer))
