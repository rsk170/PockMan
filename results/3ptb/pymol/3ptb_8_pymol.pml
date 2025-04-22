load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_8 — score 0.00
set_color pocket_8_color, [0.00, 0.00, 1.00]
select pocket_8, (resi 172 and chain A) or (resi 171 and chain A) or (resi 175 and chain A) or (resi 173 and chain A) or (resi 224 and chain A)
show surface, pocket_8
set transparency, 0.0, pocket_8
color pocket_8_color, pocket_8

