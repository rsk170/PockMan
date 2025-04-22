load ../../pdb_files/3htb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_1 — score 1.00
set_color pocket_1_color, [1.00, 0.00, 0.00]
select pocket_1, (resi 77 and chain A) or (resi 74 and chain A) or (resi 81 and chain A) or (resi 108 and chain A) or (resi 111 and chain A) or (resi 75 and chain A) or (resi 107 and chain A) or (resi 84 and chain A) or (resi 76 and chain A) or (resi 78 and chain A) or (resi 103 and chain A) or (resi 73 and chain A) or (resi 80 and chain A)
show surface, pocket_1
set transparency, 0.0, pocket_1
color pocket_1_color, pocket_1

