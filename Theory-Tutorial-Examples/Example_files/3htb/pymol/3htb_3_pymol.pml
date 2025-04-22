load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_3 — score 0.67
set_color pocket_3_color, [0.67, 0.00, 0.33]
select pocket_3, (resi 118 and chain A) or (resi 119 and chain A) or (resi 121 and chain A) or (resi 122 and chain A) or (resi 123 and chain A) or (resi 120 and chain A) or (resi 115 and chain A) or (resi 87 and chain A)
show surface, pocket_3
set transparency, 0.0, pocket_3
color pocket_3_color, pocket_3

