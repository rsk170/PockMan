load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_8 — score 0.00
set_color pocket_8_color, [0.00, 0.00, 1.00]
select pocket_8, (resi 19 and chain A) or (resi 23 and chain A) or (resi 34 and chain A) or (resi 37 and chain A) or (resi 35 and chain A) or (resi 36 and chain A) or (resi 25 and chain A) or (resi 38 and chain A) or (resi 24 and chain A)
show surface, pocket_8
set transparency, 0.0, pocket_8
color pocket_8_color, pocket_8

