########################################################################
###	FreeFEM mesh format
########################################################################

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

		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
			for node_id in node_list:
				coord = cubit.get_nodal_coordinates(node_id)
				fid.write(f'{coord[0]} {coord[1]} {coord[2]} {0}\n')

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

########################################################################
###	Gmsh format version 2
########################################################################

def export_3D_gmsh_ver2(cubit, FileName):

	with open(FileName, 'w') as fid:

		fid.write("$MeshFormat\n")
		fid.write("2.2 0 8\n")
		fid.write("$EndMeshFormat\n")

		fid.write("$PhysicalNames\n")
		fid.write(f'{cubit.get_nodeset_count() + cubit.get_block_count()}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'2 {nodeset_id} "{name}"\n')

		for block_id in cubit.get_block_id_list():
			name = cubit.get_exodus_entity_name("block",block_id)
			fid.write(f'3 {block_id} "{name}"\n')
		fid.write('$EndPhysicalNames\n')

		fid.write("$Nodes\n")

		node_list = []
		for block_id in cubit.get_block_id_list():
			volume_list = cubit.get_block_volumes(block_id)
			node_list += cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		fid.write(f'{len(node_list}\n')
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f'{node_id} {coord[0]} {coord[1]} {coord[2]}\n')
		fid.write('$EndNodes\n')

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

		fid.close()
	return cubit

########################################################################
###	Gmsh format version 4
########################################################################

def export_3D_gmsh_ver4(cubit, FileName):

	nodeset_vertex_count = 0
	nodeset_curve_count = 0
	nodeset_surface_count = 0
	for nodeset_id in cubit.get_nodeset_id_list():
		surface_list = cubit.get_nodeset_surfaces(nodeset_id)
		for surface_id in surface_list:
			nodeset_surface_count += 1
			nodeset_vertex_count += len(cubit.get_relatives("surface", surface_id, "vertex"))
			nodeset_curve_count += len(cubit.get_relatives("surface", surface_id, "curve"))

	block_volume_count = 0
	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		for volume_id in volume_list:
			block_volume_count += 1

	with open(FileName, 'w') as fid:

		fid.write('$MeshFormat\n')
		fid.write('4.1 0 8\n')
		fid.write('$EndMeshFormat\n')

		fid.write('$PhysicalNames\n')
		fid.write(f'{3*cubit.get_nodeset_count() + cubit.get_block_count()}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'0 {nodeset_id} "{name}_vertex"\n')
		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'1 {nodeset_id} "{name}_curve"\n')
		for nodeset_id in cubit.get_nodeset_id_list():
			name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
			fid.write(f'2 {nodeset_id} "{name}"\n')
		for block_id in cubit.get_block_id_list():
			name = cubit.get_exodus_entity_name("block",block_id)
			fid.write(f'3 {block_id} "{name}"\n')
		fid.write('$EndPhysicalNames\n')

		fid.write('$Entities\n')
		fid.write(f'{nodeset_vertex_count} {nodeset_curve_count} {nodeset_surface_count} {block_volume_count}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				vertex_list = cubit.get_relatives("surface", surface_id, "vertex")
				for vertex_id in vertex_list:
					x = cubit.vertex(vertex_id).coordinates()[0]
					y = cubit.vertex(vertex_id).coordinates()[1]
					z = cubit.vertex(vertex_id).coordinates()[2]
					fid.write(f'{vertex_id} {x} {y} {z} {1} {nodeset_id}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				for curve_id in curve_list:
					bounding_box = cubit.get_bounding_box("curve", curve_id)
					minx = bounding_box[0]
					maxx = bounding_box[1]
					miny = bounding_box[3]
					maxy = bounding_box[4]
					minz = bounding_box[6]
					maxz = bounding_box[7]
					vertex_list = cubit.get_relatives("curve", curve_id, "vertex")
					fid.write(f'{curve_id} {minx} {miny} {minz} {maxx} {maxy} {maxz} {1} {nodeset_id} {len(vertex_list)}')
					for vertex_id in vertex_list:
						fid.write(f' {vertex_id}')
					fid.write(f'\n')

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
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				fid.write(f'{surface_id} {minx} {miny} {minz} {maxx} {maxy} {maxz} {1} {nodeset_id} {len(curve_list)}\n')
				for curve_id in curve_list:
						fid.write(f' {curve_id}')
				fid.write(f'\n')

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
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

		node_all_list = []
		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				vertex_list = cubit.get_relatives("surface", surface_id, "vertex")
				for vertex_id in vertex_list:
					node_id = cubit.get_vertex_node(vertex_id)
					node_all_list += [node_id]

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				for curve_id in curve_list:
					node_list = cubit.get_curve_nodes(curve_id)
					node_all_list += node_list

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				node_list = cubit.get_surface_nodes(surface_id)
				node_all_list += node_list

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				node_list = cubit.parse_cubit_list( "node", f"in volume {volume_id}" )
				node_all_list += node_list

		fid.write('$Nodes\n')
		fid.write(f'{nodeset_vertex_count + nodeset_curve_count + nodeset_surface_count + block_volume_count} {len(node_all_list)} 1 {cubit.get_node_count()}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				vertex_list = cubit.get_relatives("surface", surface_id, "vertex")
				for vertex_id in vertex_list:
					node_id = cubit.get_vertex_node(vertex_id)
					fid.write(f'0 {vertex_id} 0 1\n')
					fid.write(f'{node_id}\n')
					coord = cubit.get_nodal_coordinates(node_id)
					fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				for curve_id in curve_list:
					node_list = cubit.get_curve_nodes(curve_id)
					fid.write(f'1 {curve_id} 0 {len(node_list)}\n')
					for node_id in node_list:
						fid.write(f'{node_id}\n')
					for node_id in node_list:
						coord = cubit.get_nodal_coordinates(node_id)
						fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				node_list = cubit.get_surface_nodes(surface_id)
				fid.write(f'2 {surface_id} 0 {len(node_list)}\n')
				for node_id in node_list:
					fid.write(f'{node_id}\n')
				for node_id in node_list:
					coord = cubit.get_nodal_coordinates(node_id)
					fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				node_list = cubit.parse_cubit_list( "node", f"in volume {volume_id}" )
				fid.write(f'3 {volume_id} 0 {len(node_list)}\n')
				for node_id in node_list:
					fid.write(f'{node_id}\n')
				for node_id in node_list:
					coord = cubit.get_nodal_coordinates(node_id)
					fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')
		fid.write('$EndNodes\n')

		vertex_all_list = []
		edge_all_list = []
		tri_all_list = []
		quad_all_list = []
		tet_all_list = []
		hex_all_list = []
		wedge_all_list = []

		fid.write('$Elements\n')
		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				vertex_list = cubit.get_relatives("surface", surface_id, "vertex")
				for vertex_id in vertex_list:
					vertex_all_list += [cubit.get_vertex_node(vertex_id)]

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				for curve_id in curve_list:
					edge_all_list += cubit.get_curve_edges(curve_id)

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

		elementTag = 0

		all_list = vertex_all_list + edge_all_list + hex_all_list + tet_all_list  + wedge_all_list + quad_all_list + tri_all_list
		fid.write(f'{nodeset_vertex_count + nodeset_curve_count + nodeset_surface_count + block_volume_count} {len(all_list)} {min(all_list)} {max(all_list)}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				vertex_list = cubit.get_relatives("surface", surface_id, "vertex")
				for vertex_id in vertex_list:
					node_id = cubit.get_vertex_node(vertex_id)
					fid.write(f'0 {vertex_id} 15 1\n')
					elementTag +=1
					fid.write(f'{elementTag} {node_id}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				curve_list = cubit.get_relatives("surface", surface_id, "curve")
				for curve_id in curve_list:
					edge_list = cubit.get_curve_edges(curve_id)
					if len(edge_list)>0:
						fid.write(f'1 {curve_id} 1 {len(edge_list)}\n')
						for edge_id in edge_list:
							connectivity_list = cubit.get_connectivity("edge", edge_id)
							elementTag +=1
							fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]}\n')

		for nodeset_id in cubit.get_nodeset_id_list():
			surface_list = cubit.get_nodeset_surfaces(nodeset_id)
			for surface_id in surface_list:
				tri_list = cubit.get_surface_tris(surface_id)
				if len(tri_list)>0:
					fid.write(f'2 {surface_id} 2 {len(tri_list)}\n')
					for tri_id in tri_list:
						connectivity_list = cubit.get_connectivity("tri", tri_id)
						elementTag +=1
						fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]}\n')

				quad_list = cubit.get_surface_quads(surface_id)
				if len(quad_list)>0:
					fid.write(f'2 {surface_id} 3 {len(quad_list)}\n')
					for quad_id in quad_list:
						connectivity_list = cubit.get_connectivity("quad", quad_id)
						elementTag +=1
						fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

		for block_id in cubit.get_block_id_list():
			for volume_id in cubit.get_block_volumes(block_id):
				tet_list = cubit.get_volume_tets(volume_id)
				if len(tet_list)>0:
					fid.write(f'3 {volume_id} 4 {len(tet_list)}\n')
					for tet_id in tet_list:
						connectivity_list = cubit.get_connectivity("tet", tet_id)
						elementTag +=1
						fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

				hex_list = cubit.get_volume_hexes(volume_id)
				if len(hex_list)>0:
					fid.write(f'3 {volume_id} 5 {len(hex_list)}\n')
					for hex_id in hex_list:
						connectivity_list = cubit.get_connectivity("hex", hex_id)
						elementTag +=1
						fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {connectivity_list[4]} {connectivity_list[5]} {connectivity_list[6]} {connectivity_list[7]}\n')

				wedge_list = cubit.get_volume_wedges(volume_id)
				if len(wedge_list)>0:
					fid.write(f'3 {volume_id} 6 {len(wedge_list)}\n')
					for wedge_id in wedge_list:
						connectivity_list = cubit.get_connectivity("wedge", wedge_id)
						elementTag +=1
						fid.write(f'{elementTag} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n')

		fid.write('$EndElements\n')
		fid.close()
	return cubit

########################################################################
###	NASTRAN 2D file
########################################################################

def export_2D_Nastran(cubit, FileName):
	import datetime
	formatted_date_time = datetime.datetime.now().strftime("%d-%b-%y at %H:%M:%S")

	fid = open(FileName,'w',encoding='UTF-8')
	fid.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
	fid.write("$\n")
	fid.write("$                         CUBIT version 2023.8 NX Nastran Translator\n")
	fid.write("$\n")
	fid.write("f$            File: {FileName}\n")
	fid.write(f"$      Time Stamp: {formatted_date_time}\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$                        PLEASE CHECK YOUR MODEL FOR UNITS CONSISTENCY.\n")
	fid.write("$\n")
	fid.write("$       It should be noted that load ID's from CUBIT may NOT correspond to Nastran SID's\n")
	fid.write("$ The SID's for the load and restraint sets start at one and increment by one:i.e.,1,2,3,4...\n")
	fid.write("$\n")
	fid.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ -------------------------\n")
	fid.write("$ Executive Control Section\n")
	fid.write("$ -------------------------\n")
	fid.write("$\n")
	fid.write("SOL 101\n")
	fid.write("CEND\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ --------------------\n")
	fid.write("$ Case Control Section\n")
	fid.write("$ --------------------\n")
	fid.write("$\n")
	fid.write("ECHO = SORT\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Initial\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Default Set\n")
	fid.write("$\n")
	fid.write("SUBCASE = 1\n")
	fid.write("$\n")
	fid.write("LABEL = Default Set\n")
	fid.write("$\n")
	fid.write("$ -----------------\n")
	fid.write("$ Bulk Data Section\n")
	fid.write("$ -----------------\n")
	fid.write("$\n")
	fid.write("BEGIN BULK\n")
	fid.write("$\n")
	fid.write("$ Params\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Node cards\n")
	fid.write("$\n")

	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f"GRID    {node_id:<8}{0:<8}{coord[0]:> 7.5f}{coord[1]:> 7.5f}{coord[2]:> 7.5f}\n")
	fid.write("$\n")
	fid.write("$ Element cards\n")
	fid.write("$\n")
	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block",block_id)
		fid.write("$\n")
		fid.write(f"$ Name: {name}\n")
		fid.write("$\n")
		surface_list = cubit.get_block_surfaces(block_id)
		for surface_id in surface_list:
			tri_list = cubit.get_surface_tris(surface_id)
			for tri_id in tri_list:
				node_list = cubit.get_connectivity('tri',tri_id)
				coord1 = cubit.get_nodal_coordinates(node_list[0])
				coord2 = cubit.get_nodal_coordinates(node_list[1])
				coord3 = cubit.get_nodal_coordinates(node_list[2])
				x1 = coord1[0]
				y1 = coord1[1]
				x2 = coord2[0]
				y2 = coord2[1]
				x3 = coord3[0]
				y3 = coord3[1]
				x21 = x2-x1
				y21 = y2-y1
				x31 = x3-x1
				y31 = y3-y1
				z_cross = x21*y31-x31*y21
				if z_cross > 0:
					fid.write(f"CTRIA3  {tri_id:<8}{block_id:<8}{node_list[0]:<8}{node_list[1]:<8}{node_list[2]:<8}\n")
				else:
					fid.write(f"CTRIA3  {tri_id:<8}{block_id:<8}{node_list[0]:<8}{node_list[2]:<8}{node_list[1]:<8}\n")
	fid.write("$\n")
	fid.write("$ Property cards\n")
	fid.write("$\n")
	
	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block",block_id)
		fid.write("$\n")
		fid.write(f"$ Name: {name}\n")
		fid.write("$\n")
		fid.write(f"PSHELL  {block_id:< 8}100     1       \n")
	fid.write("$\n")
	fid.write("$ Material cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Default-Steel\n")
	fid.write("$\n")
	fid.write("MAT1*   100             206800          80155.039       0.29            \n")
	fid.write("*       7e-06           1.2e-05         \n")
	fid.write("$\n")
	fid.write("$ Restraint cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Load cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("ENDDATA\n")
	fid.close()
	return cubit

def export_3D_Nastran(cubit, FileName):

	import datetime
	formatted_date_time = datetime.datetime.now().strftime("%d-%b-%y at %H:%M:%S")
	fid = open(FileName,'w',encoding='UTF-8')
	fid.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
	fid.write("$\n")
	fid.write("$                         CUBIT version 2023.8 NX Nastran Translator\n")
	fid.write("$\n")
	fid.write("f$            File: {FileName}\n")
	fid.write(f"$      Time Stamp: {formatted_date_time}\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$                        PLEASE CHECK YOUR MODEL FOR UNITS CONSISTENCY.\n")
	fid.write("$\n")
	fid.write("$       It should be noted that load ID's from CUBIT may NOT correspond to Nastran SID's\n")
	fid.write("$ The SID's for the load and restraint sets start at one and increment by one:i.e.,1,2,3,4...\n")
	fid.write("$\n")
	fid.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ -------------------------\n")
	fid.write("$ Executive Control Section\n")
	fid.write("$ -------------------------\n")
	fid.write("$\n")
	fid.write("SOL 101\n")
	fid.write("CEND\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ --------------------\n")
	fid.write("$ Case Control Section\n")
	fid.write("$ --------------------\n")
	fid.write("$\n")
	fid.write("ECHO = SORT\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Initial\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Default Set\n")
	fid.write("$\n")
	fid.write("SUBCASE = 1\n")
	fid.write("$\n")
	fid.write("LABEL = Default Set\n")
	fid.write("$\n")
	fid.write("$ -----------------\n")
	fid.write("$ Bulk Data Section\n")
	fid.write("$ -----------------\n")
	fid.write("$\n")
	fid.write("BEGIN BULK\n")
	fid.write("$\n")
	fid.write("$ Params\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Node cards\n")
	fid.write("$\n")
	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f"GRID*   {node_id:>16}{0:>16}{coord[0]:>16.5f}{coord[1]:>16.5f}\n*       {coord[2]:>16.5f}\n")
	fid.write("$\n")
	fid.write("$ Element cards\n")
	fid.write("$\n")
	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block",block_id)
		fid.write("$\n")
		fid.write(f"$ Name: {name}\n")
		fid.write("$\n")
		volume_list = cubit.get_block_volumes(block_id)
		for volume_id in volume_list:
			tet_list = cubit.get_volume_tets(volume_id)
			for tet_id in tet_list:
				node_list = cubit.get_connectivity('tet',tet_id)
				fid.write(f"CTETRA  {tet_id:>8}{block_id:>8}{node_list[0]:>8}{node_list[1]:>8}{node_list[2]:>8}{node_list[3]:>8}\n")
			hex_list = cubit.get_volume_hexes(volume_id)
			for hex_id in hex_list:
				node_list = cubit.get_connectivity('hex',hex_id)
				fid.write(f"CHEXA   {hex_id:>8}{block_id:>8}{node_list[0]:>8}{node_list[1]:>8}{node_list[2]:>8}{node_list[3]:>8}{node_list[4]:>8}{node_list[5]:>8}+\n+       {node_list[6]:>8}{node_list[7]:>8}\n")
			wedge_list = cubit.get_volume_wedges(volume_id)
			for wedge_id in wedge_list:
				node_list = cubit.get_connectivity('wedge',wedge_id)
				fid.write(f"CHEXA   {wedge_id:>8}{block_id:>8}{node_list[0]:>8}{node_list[1]:>8}{node_list[2]:>8}{node_list[3]:>8}{node_list[4]:>8}{node_list[5]:>8}\n")
			pyramid_list = cubit.get_volume_pyramids(volume_id)
			JMAG = 0
			if JMAG:
				for pyramid_id in pyramid_list:
					node_list = cubit.get_connectivity('pyramid',pyramid_id)
				fid.write(f"CHEXA   {hex_id:>8}{block_id:>8}{node_list[0]:>8}{node_list[1]:>8}{node_list[2]:>8}{node_list[3]:>8}{node_list[4]:>8}{node_list[4]:>8}+\n+       {node_list[4]:>8}{node_list[4]:>8}\n")
			else:
				for pyramid_id in pyramid_list:
					node_list = cubit.get_connectivity('pyramid',pyramid_id)
					fid.write(f"CPYRAM  {pyramid_id:>8}{block_id:>8}{node_list[0]:>8}{node_list[1]:>8}{node_list[2]:>8}{node_list[3]:>8}{node_list[4]:>8}\n")
	fid.write("$\n")
	fid.write("$ Property cards\n")
	fid.write("$\n")

	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block",block_id)
		fid.write("$\n")
		fid.write(f"$ Name: {name}\n")
		fid.write("$\n")
		fid.write(f"PSOLID  {block_id:< 8}100     1       \n")
	fid.write("$\n")
	fid.write("$ Material cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Name: Default-Steel\n")
	fid.write("$\n")
	fid.write("MAT1*   100             206800          80155.039       0.29            \n")
	fid.write("*       7e-06           1.2e-05         \n")
	fid.write("$\n")
	fid.write("$ Restraint cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$ Load cards\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("$\n")
	fid.write("ENDDATA\n")
	fid.close()
	return cubit

########################################################################
###	ELF 2D file
########################################################################

def export_2D_meg(cubit, FileName):

	fid = open(FileName,'w',encoding='UTF-8')
	fid.write("BOOK  MEP  3.50\n")
	fid.write("* ELF/MESH VERSION 7.3.0\n")
	fid.write("* SOLVER = ELF/MAGIC\n")
	fid.write("MGSC 0.001\n")
	fid.write("* NODE\n")

	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f"MGR1 {node_id} 0 {coord[0]} {coord[1]} {coord[2]}\n")

	fid.write("* ELEMENT K\n")
	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block",block_id)
		for surface_id in cubit.get_block_surfaces(block_id):

			tri_list = cubit.get_surface_tris(surface_id)
			for tri_id in tri_list:
				node_list = cubit.get_connectivity('tri',tri_id)
				fid.write(f"MMB3K {tri_id} 0 {block_id} {node_list[0]} {node_list[1]} {node_list[2]}\n")

			quad_list = cubit.get_surface_quads(surface_id)
			for quad_id in quad_list:
				node_list = cubit.get_connectivity('quad',quad_id)
				fid.write(f"MMB4K {quad_id} 0  {block_id} {node_list[0]} {node_list[1]} {node_list[2]} {node_list[3]}\n")

	fid.write("* NODE\n")
	#	fid.write(f"MGR2 {node_id} 0 {coord[0]} {coord[1]} {coord[2]}\n")
	fid.write("BOOK  END\n")
	fid.close()
	return cubit

########################################################################
###	ELF 3D file
########################################################################

def export_3D_meg(cubit, FileName):

	fid = open(FileName,'w',encoding='UTF-8')
	fid.write("BOOK  MEP  3.50\n")
	fid.write("* ELF/MESH VERSION 7.3.0\n")
	fid.write("* SOLVER = ELF/MAGIC\n")
	fid.write("MGSC 0.001\n")
	fid.write("* NODE\n")

	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f"MGR1 {node_id} 0 {coord[0]} {coord[1]} {coord[2]}\n")

	fid.write("* ELEMENT K\n")
	for block_id in cubit.get_block_id_list():
		for volume_id in cubit.get_block_volumes(block_id):
			tet_list = cubit.get_volume_tets(volume_id)
			if len(tet_list)>0:
				for tet_id in tet_list:
					node_list = cubit.get_connectivity('tet',tet_id)
					connectivity_list = cubit.get_connectivity("tet", tet_id)
					fid.write(f"MMB4T {tet_id} 0 {block_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]}\n")
			hex_list = cubit.get_volume_hexes(volume_id)
			if len(hex_list)>0:
				for hex_id in hex_list:
					connectivity_list = cubit.get_connectivity("hex", hex_id)
					fid.write(f"MMB8T {hex_id} 0 {block_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {connectivity_list[4]} {connectivity_list[5]} {connectivity_list[6]} {connectivity_list[7]}\n")
			wedge_list = cubit.get_volume_wedges(volume_id)
			if len(wedge_list)>0:
				for wedge_id in wedge_list:
					connectivity_list = cubit.get_connectivity("wedge", wedge_id)
					fid.write(f"MMB6T {hex_id} 0 {block_id} {connectivity_list[0]} {connectivity_list[1]} {connectivity_list[2]} {connectivity_list[3]} {connectivity_list[4]} {connectivity_list[5]}\n")

	fid.write("* NODE\n")
	#	fid.write(f"MGR2 {node_id} 0 {coord[0]} {coord[1]} {coord[2]}\n")
	fid.write("BOOK  END\n")
	fid.close()
	return cubit

########################################################################
###	NGSolve vol file
########################################################################

def export_3D_ngsolve(cubit, FileName):

	from netgen.csg import Pnt
	from netgen.meshing import Mesh, MeshPoint, Element3D, Element2D, Element1D, FaceDescriptor
	ngmesh = Mesh()
	ngmesh.dim = 3
	bc = {}
	pointmap = {}
	names = {}

	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			pnum = ngmesh.Add(MeshPoint(Pnt(coord[0], coord[1], coord[2])))
			pointmap[node_id] = pnum

	for nodeset_id in cubit.get_nodeset_id_list():
		name = cubit.get_exodus_entity_name("nodeset", nodeset_id)
		surface_list = cubit.get_nodeset_surfaces(nodeset_id)
		for surface_id in surface_list:
			names[surface_id] = name

	for block_id in cubit.get_block_id_list():
		name = cubit.get_exodus_entity_name("block", block_id)
		ngmesh.SetMaterial(block_id, name)

		volume_list = cubit.get_block_volumes(block_id)
		for volume_id in volume_list:
			surface_list = cubit.get_relatives("volume", volume_id, "surface")
			for surface_id in surface_list:
				bc[surface_id] = ngmesh.Add(FaceDescriptor(bc=surface_id, domin=block_id, surfnr=surface_id))
				ngmesh.SetBCName(surface_id-1, names[surface_id])

				quad_list = cubit.get_surface_quads(surface_id)
				if len(quad_list)>0:
					for quad_id in quad_list:
						connectivity_list = cubit.get_connectivity("quad", quad_id)
						ngmesh.Add(Element2D(bc[surface_id], [pointmap[connectivity_list[0]], pointmap[connectivity_list[1]], pointmap[connectivity_list[2]], pointmap[connectivity_list[3]]]))

				tri_list = cubit.get_surface_tris(surface_id)
				if len(tri_list)>0:
					for tri_id in tri_list:
						connectivity_list = cubit.get_connectivity("tri", tri_id)
						ngmesh.Add(Element2D(bc[surface_id], [pointmap[connectivity_list[0]], pointmap[connectivity_list[1]], pointmap[connectivity_list[2]]]))

				tet_list = cubit.get_volume_tets(volume_id)
				if len(tet_list)>0:
					for tet_id in tet_list:
						connectivity_list = cubit.get_connectivity("tet", tet_id)
						ngmesh.Add(Element3D(block_id, [pointmap[connectivity_list[0]], pointmap[connectivity_list[1]], pointmap[connectivity_list[2]], pointmap[connectivity_list[3]]]))

				hex_list = cubit.get_volume_hexes(volume_id)
				if len(hex_list)>0:
					for hex_id in hex_list:
						connectivity_list = cubit.get_connectivity("hex", hex_id)
						ngmesh.Add(Element3D(block_id, [pointmap[connectivity_list[0]], pointmap[connectivity_list[1]], pointmap[connectivity_list[2]], pointmap[connectivity_list[3]], pointmap[connectivity_list[4]], pointmap[connectivity_list[5]], pointmap[connectivity_list[6]], pointmap[connectivity_list[7]]]))

				wedge_list = cubit.get_volume_wedges(volume_id)
				if len(wedge_list)>0:
					for wedge_id in wedge_list:
						connectivity_list = cubit.get_connectivity("wedge", wedge_id)
						ngmesh.Add(Element3D(block_id, [pointmap[connectivity_list[0]], pointmap[connectivity_list[1]], pointmap[connectivity_list[2]], pointmap[connectivity_list[3]], pointmap[connectivity_list[4]], pointmap[connectivity_list[5]]]))

	ngmesh.Save(FileName)
	return ngmesh, cubit

########################################################################
###	vtk format
########################################################################

def export_3D_vtk(cubit, FileName):

	fid = open(FileName,'w')
	fid.write('# vtk DataFile Version 3.0\n')
	fid.write(f'Unstructured Grid {FileName}\n')
	fid.write('ASCII\n')
	fid.write('DATASET UNSTRUCTURED_GRID\n')
	fid.write(f'POINTS {cubit.get_node_count()} float\n')

	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			fid.write(f'{coord[0]} {coord[1]} {coord[2]}\n')

	tet_list = []
	hex_list = []
	wedge_list = []
	pyramid_list = []
	volume_id_list = []
	for block_id in cubit.get_block_id_list():
		for volume_id in cubit.get_block_volumes(block_id):
			tet_list += cubit.get_volume_tets(volume_id)
			volume_id_list += [volume_id]*(len(cubit.get_volume_tets(volume_id)))

	for block_id in cubit.get_block_id_list():
		for volume_id in cubit.get_block_volumes(block_id):
			hex_list += cubit.get_volume_hexes(volume_id)
			volume_id_list += [volume_id]*(len(cubit.get_volume_hexes(volume_id)))

	for block_id in cubit.get_block_id_list():
		for volume_id in cubit.get_block_volumes(block_id):
			wedge_list += cubit.get_volume_wedges(volume_id)
			volume_id_list += [volume_id]*(len(cubit.get_volume_wedges(volume_id)))
	for block_id in cubit.get_block_id_list():
		for volume_id in cubit.get_block_volumes(block_id):
			pyramid_list += cubit.get_volume_pyramids(volume_id)
			volume_id_list += [volume_id]*(len(cubit.get_volume_pyramids(volume_id)))

	fid.write(f'CELLS {len(tet_list) + len(hex_list) + len(wedge_list) + len(pyramid_list)} {5*len(tet_list) + 9*len(hex_list) + 7*len(wedge_list) + 6*len(pyramid_list)}\n' )
	for tet_id in tet_list:
		connectivity_list = cubit.get_connectivity("tet", tet_id)
		fid.write(f'4 {connectivity_list[0]-1} {connectivity_list[1]-1} {connectivity_list[2]-1} {connectivity_list[3]-1}\n')
	for hex_id in hex_list:
		connectivity_list = cubit.get_connectivity("hex", hex_id)
		fid.write(f'8 {connectivity_list[0]-1} {connectivity_list[1]-1} {connectivity_list[2]-1} {connectivity_list[3]-1} {connectivity_list[4]-1} {connectivity_list[5]-1} {connectivity_list[6]-1} {connectivity_list[7]-1}\n')
	for wedge_id in wedge_list:
		fid.write(f'6 {connectivity_list[0]-1} {connectivity_list[1]-1} {connectivity_list[2]-1} {connectivity_list[3]-1} {connectivity_list[4]-1} {connectivity_list[5]-1} \n')
	for pyramid_id in pyramid_list:
		fid.write(f'5 {connectivity_list[0]-1} {connectivity_list[1]-1} {connectivity_list[2]-1} {connectivity_list[3]-1} {connectivity_list[4]-1} \n')

	fid.write(f'CELL_TYPES {len(tet_list) + len(hex_list) + len(wedge_list) + len(pyramid_list)}\n')
	for tet_id in tet_list:
		fid.write('10\n')
	for hex_id in hex_list:
		fid.write('12\n')
	for wedge_id in wedge_list:
		fid.write('13\n')
	for pyramid_id in pyramid_list:
		fid.write('14\n')
	fid.write(f'CELL_DATA {len(tet_list) + len(hex_list) + len(wedge_list) + len(pyramid_list)}\n')
	fid.write('SCALARS scalars float\n')
	fid.write('LOOKUP_TABLE default\n')
	for volume_id in volume_id_list:
		fid.write(f'{volume_id}\n')
	fid.close()
	return cubit

########################################################################
###	Lukas FEM 2D file
########################################################################

def export_2D_geo_mesh(cubit, FileName):

	import numpy
	import scipy.io

	node_list = []

	N = cubit.get_node_count()
	M = cubit.get_tri_count()

	nodes = []
	for block_id in cubit.get_block_id_list():
		volume_list = cubit.get_block_volumes(block_id)
		node_list = cubit.parse_cubit_list( 'node', f'in volume {" ".join(map(str, volume_list)) }' )
		for node_id in node_list:
			coord = cubit.get_nodal_coordinates(node_id)
			nodes.append([coord[0],coord[1]])

	for nodeset_id in cubit.get_nodeset_id_list():
		name = cubit.get_exodus_entity_name("nodeset",nodeset_id)
		curve_list = cubit.get_nodeset_curves(nodeset_id)
		node_list = []
		for curve_id in curve_list:
			node_list += cubit.get_curve_nodes(curve_id)
		nodeset = numpy.array([(name, node_list)], dtype=[('name', 'U20'), ('DBCnodes', 'O')])
		try:
			nodesets = append(nodesets,nodeset)
		except:
			nodesets = nodeset

	conn_matrix = numpy.zeros((M,3))
	center_x = numpy.zeros((M))
	center_y = numpy.zeros((M))
	block_count = cubit.get_block_count()
	regions = numpy.rec.array([("", [], [])]*(block_count), dtype=[('name', 'U20'), ('Elements', 'O'), ('Nodes', 'O')])

	for block_id in cubit.get_block_id_list():
		Elements = []
		name = cubit.get_exodus_entity_name("block",block_id)
		surface_list = cubit.get_block_surfaces(block_id)
		Nodes = []
		Elements = []
		for surface_id in surface_list:
			tri_list = cubit.get_surface_tris(surface_id)
			Elements	+= tri_list
			for tri_id in tri_list:
				x = []
				y = []
				node_list = cubit.get_connectivity('tri',tri_id)
				Nodes += node_list
				conn_matrix[tri_id-1,:] = node_list
				for node_id in node_list:
					coord = cubit.get_nodal_coordinates(node_id)
					x.append(coord[0])
					y.append(coord[1])
				center_x[tri_id-1] = numpy.mean(x)
				center_y[tri_id-1] = numpy.mean(y)
		regions[block_id-1][0] = name
		regions[block_id-1][1] = Elements
		regions[block_id-1][2] = Nodes

	geo = {'conn_matrix':conn_matrix, 'nodes':nodes, 'M':M, 'N':N, 'nodesets':nodesets , 'center_x':center_x, 'center_y':center_y, 'regions':regions }
	scipy.io.savemat(FileName, {'geo': geo}, format='5', long_field_names=True)
	return cubit

