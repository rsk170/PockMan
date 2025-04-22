load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_13 — score 0.00
set_color pocket_13_color, [0.00, 0.00, 1.00]
select pocket_13, (resi 79 and chain A) or (resi 115 and chain A) or (resi 81 and chain A) or (resi 69 and chain A) or (resi 118 and chain A) or (resi 80 and chain A) or (resi 117 and chain A) or (resi 67 and chain A) or (resi 113 and chain A) or (resi 114 and chain A)
show surface, pocket_13
set transparency, 0.0, pocket_13
color pocket_13_color, pocket_13

