(defun which-line ()
  "Print the current line and total lines in buffer"
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos))
	(tot 0))
    (goto-char (point-min))
    (save-match-data
      (while (re-search-forward "[\n\C-m]" nil t 10)
	(setq tot (+ 10 tot)))
      (while (re-search-forward "[\n\C-m]" nil t 1)
	(setq tot (+ 1 tot))))
    (if (= start 1)
	(message "Line %d of %d" n tot)
      (save-excursion
	(save-restriction
          (widen)
          (message "line %d (narrowed line %d)"
                   (+ n (line-number-at-pos start) -1) n))))))
