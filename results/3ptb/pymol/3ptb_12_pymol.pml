load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_12 — score 0.00
set_color pocket_12_color, [0.00, 0.00, 1.00]
select pocket_12, (resi 99 and chain A) or (resi 100 and chain A) or (resi 97 and chain A) or (resi 175 and chain A) or (resi 98 and chain A) or (resi 215 and chain A) or (resi 180 and chain A)
show surface, pocket_12
set transparency, 0.0, pocket_12
color pocket_12_color, pocket_12

