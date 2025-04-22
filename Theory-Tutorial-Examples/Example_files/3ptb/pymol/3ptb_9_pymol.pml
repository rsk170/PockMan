load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_9 — score 0.00
set_color pocket_9_color, [0.00, 0.00, 1.00]
select pocket_9, (resi 192 and chain A) or (resi 191 and chain A) or (resi 143 and chain A) or (resi 149 and chain A) or (resi 193 and chain A) or (resi 151 and chain A)
show surface, pocket_9
set transparency, 0.0, pocket_9
color pocket_9_color, pocket_9

