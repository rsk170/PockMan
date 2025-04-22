load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_7 — score 0.00
set_color pocket_7_color, [0.00, 0.00, 1.00]
select pocket_7, (resi 88A and chain A) or (resi 84A and chain A) or (resi 186 and chain A) or (resi 225 and chain A) or (resi 185 and chain A) or (resi 184 and chain A) or (resi 187 and chain A) or (resi 163 and chain A) or (resi 188 and chain A) or (resi 183 and chain A)
show surface, pocket_7
set transparency, 0.0, pocket_7
color pocket_7_color, pocket_7

