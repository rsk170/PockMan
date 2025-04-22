load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_4 — score 0.67
set_color pocket_4_color, [0.67, 0.00, 0.33]
select pocket_4, (resi 159 and chain A) or (resi 161 and chain A) or (resi 158 and chain A) or (resi 1 and chain A) or (resi 162 and chain A) or (resi 157 and chain A) or (resi 160 and chain A)
show surface, pocket_4
set transparency, 0.0, pocket_4
color pocket_4_color, pocket_4

