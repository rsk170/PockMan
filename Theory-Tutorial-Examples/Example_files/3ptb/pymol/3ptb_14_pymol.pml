load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_14 — score 0.00
set_color pocket_14_color, [0.00, 0.00, 1.00]
select pocket_14, (resi 239 and chain A) or (resi 47 and chain A) or (resi 123 and chain A) or (resi 243 and chain A) or (resi 242 and chain A) or (resi 48 and chain A) or (resi 238 and chain A) or (resi 240 and chain A) or (resi 241 and chain A)
show surface, pocket_14
set transparency, 0.0, pocket_14
color pocket_14_color, pocket_14

