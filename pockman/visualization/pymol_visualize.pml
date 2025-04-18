from pymol import cmd
cmd.load("1ppb.pdb")
cmd.show("cartoon")
cmd.color("gray50")

cmd.load("1ppb.pdb_pockets.pdb")
stored.list=[]
cmd.iterate("(resn POK)","stored.list.append(resi)")    
firstPOK=stored.list[0]  
lastPOK=stored.list[-1]  
cmd.hide("everything", "resn POK")
cmd.show("surface", "resn POK")
cmd.set("transparency", 0.3, "resn POK")
for pocket_number in stored.list: cmd.select("pocket"+str(pocket_number), "resn POK and resi "+str(pocket_number))
center resname POK and resid 1 ; zoom center, 15
util.chainbow('resname POK')
