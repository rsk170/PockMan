load ../../pdb_files/3ptb.pdb
hide everything
show surface
color grey80
bg_color black
# pocket_6 — score 0.25
set_color pocket_6_color, [0.25, 0.00, 0.75]
select pocket_6, (resi 18 and chain A) or (resi 158 and chain A) or (resi 21 and chain A) or (resi 156 and chain A) or (resi 189 and chain A) or (resi 157 and chain A) or (resi 16 and chain A) or (resi 152 and chain A) or (resi 144 and chain A) or (resi 19 and chain A) or (resi 141 and chain A) or (resi 143 and chain A) or (resi 154 and chain A) or (resi 17 and chain A) or (resi 20 and chain A) or (resi 155 and chain A) or (resi 194 and chain A) or (resi 140 and chain A) or (resi 142 and chain A)
show surface, pocket_6
set transparency, 0.0, pocket_6
color pocket_6_color, pocket_6

