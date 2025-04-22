load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_6 — score 0.00
set_color pocket_6_color, [0.00, 0.00, 1.00]
select pocket_6, (resi 130 and chain A) or (resi 150 and chain A) or (resi 151 and chain A) or (resi 154 and chain A) or (resi 155 and chain A) or (resi 152 and chain A)
show surface, pocket_6
set transparency, 0.0, pocket_6
color pocket_6_color, pocket_6

