load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_7 — score 0.00
set_color pocket_7_color, [0.00, 0.00, 1.00]
select pocket_7, (resi 129 and chain A) or (resi 128 and chain A) or (resi 123 and chain A) or (resi 120 and chain A) or (resi 125 and chain A)
show surface, pocket_7
set transparency, 0.0, pocket_7
color pocket_7_color, pocket_7

