load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_11 — score 0.00
set_color pocket_11_color, [0.00, 0.00, 1.00]
select pocket_11, (resi 235 and chain A) or (resi 124 and chain A) or (resi 128 and chain A) or (resi 210 and chain A) or (resi 231 and chain A) or (resi 232 and chain A) or (resi 123 and chain A) or (resi 125 and chain A) or (resi 127 and chain A) or (resi 233 and chain A) or (resi 204 and chain A)
show surface, pocket_11
set transparency, 0.0, pocket_11
color pocket_11_color, pocket_11

