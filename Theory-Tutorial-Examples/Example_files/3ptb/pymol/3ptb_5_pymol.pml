load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_5 — score 0.52
set_color pocket_5_color, [0.52, 0.00, 0.48]
select pocket_5, (resi 61 and chain A) or (resi 65 and chain A) or (resi 37 and chain A) or (resi 58 and chain A) or (resi 107 and chain A) or (resi 62 and chain A) or (resi 59 and chain A) or (resi 104 and chain A) or (resi 64 and chain A) or (resi 63 and chain A) or (resi 34 and chain A) or (resi 106 and chain A) or (resi 85 and chain A) or (resi 60 and chain A) or (resi 33 and chain A) or (resi 41 and chain A) or (resi 87 and chain A) or (resi 88 and chain A) or (resi 105 and chain A)
show surface, pocket_5
set transparency, 0.0, pocket_5
color pocket_5_color, pocket_5

