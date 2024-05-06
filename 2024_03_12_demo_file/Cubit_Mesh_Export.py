def export_3D_mesh(cubit, FileName):

	block_count = cubit.get_block_count()
	block_list = cubit.get_block_id_list()
	sideset_count = cubit.get_sideset_count()
	sideset_list = cubit.get_sideset_id_list()
	nodeset_count = cubit.get_nodeset_count()
	nodeset_list = cubit.get_nodeset_id_list()

	node_count = cubit.get_node_count()
	volume_count = cubit.get_volume_count()
	volume_list = cubit.get_entities("volume")
	nodeset_surface_count = 0
	nodeset_surface_list = []
	sideset_surface_list = []
	surface_sideset_id = {}
	surface_nodeset_id = {}

	with open(FileName, 'w') as fid:
		fid.write("MeshVersionFormatted 2\n")
		fid.write("\n")
		fid.write("Dimension 3\n")
		fid.write("\n")
		fid.write("Vertices\n")
		fid.write(f'{node_count}\n')

		for node_id in range(node_count+1):
			coord = cubit.get_nodal_coordinates(node_id)
			if cubit.get_node_exists(node_id):
				fid.write(f'{coord[0]} {coord[1]} {coord[2]} {0}\n')
			else:
				print(f"node {node_id} does not exist")

		fid.write("\n")
		tet_list = []
		fid.write("Tetrahedra\n")
		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			for volume_id in volume_list:
				tet_list += cubit.get_volume_tets(volume_id)
		fid.write(f'{len(tet_list)}\n')

		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			for volume_id in volume_list:
				tet_list = cubit.get_volume_tets(volume_id)
				if len(tet_list)>0:
					for tet_id in tet_list:
						connectivity_list = cubit.get_connectivity("tet", tet_id)
						fid.write(f'{connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {block_id}\n')

		tri_list = []
		fid.write("Triangles\n")
		for nodeset_id in nodeset_list:
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				tri_list += cubit.get_surface_tris(surface_id)
		fid.write(f'{len(tri_list)}\n')
		for nodeset_id in nodeset_list:
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				tri_list = cubit.get_surface_tris(surface_id)
				if len(tri_list)>0:
					for tri_id in tri_list:
						connectivity_list = cubit.get_connectivity("tri", tri_id)
						fid.write(f'{connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {nodeset_id}\n')
		for surface_id in nodeset_surface_list:
			quad_list += cubit.get_surface_quads(surface_id)
			tri_list += cubit.get_surface_tris(surface_id)

		fid.write("\n")
		fid.write("End\n")
		fid.close()
	return cubit

def export_3D_gmsh_ver2(cubit, FileName):

	with open(FileName, 'w') as fid:

########################################################################

		fid.write("$MeshFormat\n")
		fid.write("2.2 0 8\n")
		fid.write("$EndMeshFormat\n")

########################################################################

		fid.write("$PhysicalNames\n")
		fid.write(f'{cubit.get_nodeset_count() + cubit.get_block_count()}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'2 {nodeset_id} "{name}"\n')

		for block_id in cubit.get_block_id_list():
			name = cubit.get_exodus_entity_name("block",block_id)
			fid.write(f'3 {block_id} "{name}"\n')
		fid.write('$EndPhysicalNames\n')

########################################################################

		fid.write("$Nodes\n")
		fid.write(f'{cubit.get_node_count()}\n')
		for node_id in range(cubit.get_node_count()+1):
			coord = cubit.get_nodal_coordinates(node_id)
			if cubit.get_node_exists(node_id):
				fid.write(f'{node_id} {coord[0]} {coord[1]} {coord[2]}\n')
			else:
				print(f"node {node_id} does not exist")
		fid.write('$EndNodes\n')

########################################################################

		hex_list = []
		tet_list = []
		wedge_list = []
		quad_list = []
		tri_list = []
		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			for volume_id in volume_list:
				hex_list += cubit.get_volume_hexes(volume_id)
				tet_list += cubit.get_volume_tets(volume_id)
				wedge_list += cubit.get_volume_wedges(volume_id)

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				quad_list += cubit.get_surface_quads(surface_id)
				tri_list += cubit.get_surface_tris(surface_id)

		Elems = 0
		fid.write('$Elements\n')
		fid.write(f'{len(hex_list)+len(tet_list)+len(wedge_list)+len(quad_list)+len(tri_list)}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				quad_list = cubit.get_surface_quads(surface_id)
				if len(quad_list)>0:
					for quad_id in quad_list:
						Elems += 1
						connectivity_list = cubit.get_connectivity("quad", quad_id)
						fid.write(f'{Elems} {3} {2} {nodeset_id} {surface_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')
				tri_list = cubit.get_surface_tris(surface_id)
				if len(tri_list)>0:
					for tri_id in tri_list:
						Elems += 1
						connectivity_list = cubit.get_connectivity("tri", tri_id)
						fid.write(f'{Elems} {2} {2} {nodeset_id} {surface_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]}\n')

		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			for volume_id in volume_list:
				hex_list += cubit.get_volume_hexes(volume_id)
				if len(hex_list)>0:
					for hex_id in hex_list:
						Elems += 1
						connectivity_list = cubit.get_connectivity("hex", hex_id)
						fid.write(f'{Elems} {5} {2} {block_id} {volume_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {connectivity_list[4]} {connectivity_list[5]} {connectivity_list[6]} {connectivity_list[7]}\n')

				tet_list = cubit.get_volume_tets(volume_id)
				if len(tet_list)>0:
					for tet_id in tet_list:
						Elems += 1
						connectivity_list = cubit.get_connectivity("tet", tet_id)
						fid.write(f'{Elems} {4} {2} {block_id} {volume_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

				wedge_list = cubit.get_volume_wedges(volume_id)
				if len(wedge_list)>0:
					for wedge_id in wedge_list:
						Elems += 1
						connectivity_list = cubit.get_connectivity("wedge", wedge_id)
						fid.write(f'{wedge_id} {6} {2} {block_id} {volume_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')
		fid.write('$EndElements\n')

########################################################################

		fid.close()
	return cubit


def export_3D_gmsh_ver4(cubit, FileName):

	nodeset_surface_count = 0
	for nodeset_id in cubit.get_nodeset_id_list():
		surface_list = cubit.get_nodeset_surfaces(nodeset_id)
		for surface_id in surface_list:
			nodeset_surface_count += 1

	block_volume_count = 0
	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		for volume_id in volume_list:
			block_volume_count += 1

	with open(FileName, 'w') as fid:

########################################################################

		fid.write('$MeshFormat\n')
		fid.write('4.1 0 8\n')
		fid.write('$EndMeshFormat\n')

########################################################################

		fid.write('$PhysicalNames\n')
		fid.write(f'{cubit.get_nodeset_count() + cubit.get_block_count()}\n')
		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'2 {nodeset_id} "{name}"\n')
		for block_id in cubit.get_block_id_list():
			name = cubit.get_exodus_entity_name("block",block_id)
			fid.write(f'3 {block_id} "{name}"\n')
		fid.write('$EndPhysicalNames\n')

########################################################################

		fid.write('$Entities\n')
		fid.write(f'{0} {0} {nodeset_surface_count} {block_volume_count}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				bounding_box = cubit.get_bounding_box("surface", surface_id)
				minx = bounding_box[0]
				maxx = bounding_box[1]
				miny = bounding_box[3]
				maxy = bounding_box[4]
				minz = bounding_box[6]
				maxz = bounding_box[7]
				fid.write(f'{surface_id} {minx} {miny} {minz} {maxx} {maxy} {maxz} {1} {nodeset_id} {0}\n')

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				block_id = cubit.get_block_id("volume",volume_id)
				bounding_box = cubit.get_bounding_box("volume", volume_id)
				minx = bounding_box[0]
				maxx = bounding_box[1]
				miny = bounding_box[3]
				maxy = bounding_box[4]
				minz = bounding_box[6]
				maxz = bounding_box[7]
				fid.write(f'{volume_id} {minx} {miny} {minz} {maxx} {maxy} {maxz} {1} {block_id} {nodeset_surface_count}')
				for nodeset_id in cubit.get_nodeset_id_list():
					surface_list = cubit.get_nodeset_surfaces(nodeset_id)
					for surface_id in surface_list:
						fid.write(f' {surface_id}')
				fid.write(f'\n')

		fid.write('$EndEntities\n')

########################################################################

		fid.write('$Nodes\n')
		fid.write(f'{1} {cubit.get_node_count()} 1 {cubit.get_node_count()}\n')
		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				fid.write(f'3 {volume_id} 0 {cubit.get_node_count()}\n')
				for node_id in range(cubit.get_node_count()):
					fid.write(f'{node_id+1}\n')
				for node_id in range(cubit.get_node_count()+1):
					coord = cubit.get_nodal_coordinates(node_id)
					if cubit.get_node_exists(node_id):
						fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')
					else:
						print(f"node {node_id} does not exist")
		fid.write('$EndNodes\n')

########################################################################

		tri_all_list = []
		quad_all_list = []
		tet_all_list = []
		hex_all_list = []
		wedge_all_list = []

		fid.write('$Elements\n')
		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				tri_all_list += cubit.get_surface_tris(surface_id)
				quad_all_list += cubit.get_surface_quads(surface_id)

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				tet_all_list += cubit.get_volume_tets(volume_id)
				hex_all_list += cubit.get_volume_hexes(volume_id)
				wedge_all_list += cubit.get_volume_wedges(volume_id)

		all_list = hex_all_list + tet_all_list  + wedge_all_list + quad_all_list + tri_all_list
		fid.write(f'{nodeset_surface_count + block_volume_count} {len(tri_all_list)+len(quad_all_list)+len(tet_all_list)+len(hex_all_list)+len(wedge_all_list)} {min(all_list)} {max(all_list)}\n')

		elements = 0

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				tri_list = cubit.get_surface_tris(surface_id)
				if len(tri_list)>0:
					fid.write(f'2 {surface_id} 2 {len(tri_list)}\n')
					for tri_id in tri_list:
						connectivity_list = cubit.get_connectivity("tri", tri_id)
						elements +=1
						fid.write(f'{elements} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]}\n')

				quad_list = cubit.get_surface_quads(surface_id)
				if len(quad_list)>0:
					fid.write(f'2 {surface_id} 3 {len(quad_list)}\n')
					for quad_id in quad_list:
						connectivity_list = cubit.get_connectivity("quad", quad_id)
						elements +=1
						fid.write(f'{elements} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				tet_list = cubit.get_volume_tets(volume_id)
				if len(tet_list)>0:
					fid.write(f'3 {volume_id} 4 {len(tet_list)}\n')
					for tet_id in tet_list:
						connectivity_list = cubit.get_connectivity("tet", tet_id)
						elements +=1
						fid.write(f'{elements} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

				hex_list = cubit.get_volume_hexes(volume_id)
				if len(hex_list)>0:
					fid.write(f'3 {volume_id} 5 {len(hex_list)}\n')
					for hex_id in hex_list:
						connectivity_list = cubit.get_connectivity("hex", hex_id)
						elements +=1
						fid.write(f'{elements} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {connectivity_list[4]} {connectivity_list[5]} {connectivity_list[6]} {connectivity_list[7]}\n')

				wedge_list = cubit.get_volume_wedges(volume_id)
				if len(wedge_list)>0:
					fid.write(f'3 {volume_id} 6 {len(wedge_list)}\n')
					for wedge_id in wedge_list:
						connectivity_list = cubit.get_connectivity("wedge", wedge_id)
						elements +=1
						fid.write(f'{elements} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

		fid.write('$EndElements\n')
		fid.close()
	return cubit
