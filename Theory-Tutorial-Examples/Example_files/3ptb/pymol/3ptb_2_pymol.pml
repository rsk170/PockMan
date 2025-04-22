load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_2 — score 0.66
set_color pocket_2_color, [0.66, 0.00, 0.34]
select pocket_2, (resi 155 and chain A) or (resi 199 and chain A) or (resi 198 and chain A) or (resi 30 and chain A) or (resi 26 and chain A) or (resi 156 and chain A) or (resi 27 and chain A) or (resi 200 and chain A) or (resi 138 and chain A) or (resi 137 and chain A) or (resi 157 and chain A) or (resi 139 and chain A) or (resi 140 and chain A) or (resi 22 and chain A) or (resi 209 and chain A) or (resi 197 and chain A) or (resi 29 and chain A) or (resi 158 and chain A)
show surface, pocket_2
set transparency, 0.0, pocket_2
color pocket_2_color, pocket_2

