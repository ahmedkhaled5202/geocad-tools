(defun c:GCTCOUNT (/ ss idx data kind counts old row)
  (prompt "\nSelect objects to count by entity type: ")
  (setq ss (ssget))
  (if ss
    (progn
      (setq idx 0 counts nil)
      (repeat (sslength ss)
        (setq data (entget (ssname ss (float idx)))
              kind (cdr (assoc 0 data)))
        (if kind
          (progn
            (setq old (assoc kind counts))
            (if old
              (setq counts (subst (cons kind (1+ (cdr old))) old counts))
              (setq counts (cons (cons kind 1) counts)))))
        (setq idx (1+ idx)))
      (princ "\n--- GeoCAD Tools: Entity Count ---")
      (foreach row (reverse counts)
        (princ (strcat "\n" (car row) ": " (itoa (cdr row)))))
      (princ (strcat "\nTotal selected: " (itoa (sslength ss)))))
    (prompt "\nNo objects selected."))
  (princ))
(princ)
