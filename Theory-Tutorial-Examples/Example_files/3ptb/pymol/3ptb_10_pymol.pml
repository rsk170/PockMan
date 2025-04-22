load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_10 — score 0.00
set_color pocket_10_color, [0.00, 0.00, 1.00]
select pocket_10, (resi 159 and chain A) or (resi 137 and chain A) or (resi 136 and chain A) or (resi 160 and chain A) or (resi 161 and chain A) or (resi 135 and chain A) or (resi 158 and chain A)
show surface, pocket_10
set transparency, 0.0, pocket_10
color pocket_10_color, pocket_10

