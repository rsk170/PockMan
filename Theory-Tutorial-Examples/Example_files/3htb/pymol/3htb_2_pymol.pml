load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_2 — score 0.67
set_color pocket_2_color, [0.67, 0.00, 0.33]
select pocket_2, (resi 126 and chain A) or (resi 124 and chain A) or (resi 95 and chain A) or (resi 92 and chain A) or (resi 121 and chain A) or (resi 90 and chain A) or (resi 91 and chain A)
show surface, pocket_2
set transparency, 0.0, pocket_2
color pocket_2_color, pocket_2

