import pyuff


def convert_to_node(dset):
    """
    2411_dsetを_nodeへ変換
    
    Parameters
    ----------
    dset : dict 
        unvファイルから取得した節点の辞書。

    Returns
    -------
    _node : dict
        IDをキーとし、性質をvaluesとした辞書。
        {
        ID:{
            'def_cs':int, 
            'disp_cs':int,
            'color':int,
            'x':float,
            'y':float,
            'z'float:
            }
        }
    """
    _node = {}
    node = dset
    for i in range(len(node['node_nums'])):
        _node[int(node['node_nums'][i])] = {
            'def_cs':int(node['def_cs'][i]),
            'disp_cs':int(node['disp_cs'][i]),
            'color':int(node['color'][i]),
            'x':node['x'][i],
            'y':node['y'][i],
            'z':node['z'][i]
            }
        
    return _node


def convert_to_element(dset):
    """
    2412_dsetを_elemへ変換
    
    Parameters
    ----------
    dset : dict 
        unvファイルから取得した要素の辞書。

    Returns
    -------
    _elem : dict
        IDをキーとし、性質をvaluesとした辞書。
        {
        ID:{
            'fe_descriptor':int, 
            'phys_table':int,
            'mat_table':int,
            'color':int,
            'nodes_nums':int,
            'nodes_nums':array-like:
            }
        }
    """
    _elem = {}
    for key in dset.keys():
        if key != 'type':
            elem = dset[key]
            for i in range(len(elem['element_nums'])):
                _elem[int(elem['element_nums'][i])] = {
                    'fe_descriptor':elem['fe_descriptor'][i],
                    'phys_table':elem['phys_table'][i],
                    'mat_table':elem['mat_table'][i], 
                    'color':elem['color'][i], 
                    'num_nodes':len(elem['nodes_nums'][i]),
                    'nodes_nums':elem['nodes_nums'][i]
                    }
                
    return _elem


def convert_to_dset(node, elem):
    """
    node, elemを2411、2412_dsetへ変換
    
    Parameters
    ----------
    node : dict 
        IDをキーとし、性質をvaluesとした節点の辞書。

    elem : dict 
        IDをキーとし、性質をvaluesとした要素の辞書。

    Returns
    -------
    [node_dset, elem_dset] : list
        unvファイルに出力できる形式。
        [node,{'type' : 2412,'triangle' : dict,'quad' : dict}]
    """
    tmp_node = {
        'node_nums':[], 
        'def_cs':[], 
        'disp_cs':[],
        'color':[],
        'x':[],
        'y':[],
        'z':[]
        }
    tmp_tri_elem = {
        'element_nums':[],
        'fe_descriptor':[],
        'phys_table':[],
        'mat_table':[],
        'color':[],
        'num_nodes':[],
        'nodes_nums':[]
        }
    tmp_quad_elem = {
        'element_nums':[],
        'fe_descriptor':[],
        'phys_table':[],
        'mat_table':[],
        'color':[],
        'num_nodes':[],
        'nodes_nums':[]
        }

    for ID in node.keys():
        tmp_node['node_nums'].append(ID)
        for k in node[ID].keys():
            tmp_node[k].append(node[ID][k])

    node_dset = pyuff.prepare_2411(
        node_nums = tmp_node['node_nums'],
        def_cs=tmp_node['def_cs'],
        disp_cs=tmp_node['disp_cs'],
        color=tmp_node['color'],
        x=tmp_node['x'],
        y=tmp_node['y'],
        z=tmp_node['z']
        )

    elem_dset = {'type':2412}

    for ID in elem.keys():
        if elem[ID]['num_nodes'] == 3:
            tmp_tri_elem['element_nums'].append(ID)
            for k in elem[ID].keys():
                tmp_tri_elem[k].append(elem[ID][k])
        elif elem[ID]['num_nodes'] == 4:
            tmp_quad_elem['element_nums'].append(ID)
            for k in elem[ID].keys():
                tmp_quad_elem[k].append(elem[ID][k])

    if len(tmp_tri_elem['element_nums']) > 0:
        elem_dset['triangle'] = pyuff.prepare_2412(
            element_nums = tmp_tri_elem['element_nums'],
            fe_descriptor=tmp_tri_elem['fe_descriptor'],
            phys_table=tmp_tri_elem['phys_table'],
            mat_table=tmp_tri_elem['mat_table'],
            color=tmp_tri_elem['color'],
            nodes_nums=tmp_tri_elem['nodes_nums']
            )

    if len(tmp_quad_elem['element_nums']) > 0:
        elem_dset['quad'] = pyuff.prepare_2412(
            element_nums = tmp_quad_elem['element_nums'],
            fe_descriptor=tmp_quad_elem['fe_descriptor'],
            phys_table=tmp_quad_elem['phys_table'],
            mat_table=tmp_quad_elem['mat_table'],
            color=tmp_quad_elem['color'],
            nodes_nums=tmp_quad_elem['nodes_nums']
            )

    return [node_dset, elem_dset]


if __name__=="__main__":
    org_unv_file = './triangle_quad.unv'
    copy_unv_file = './copy.unv'

    unv_read = pyuff.UFF(org_unv_file)
    n_set = unv_read.read_sets(setn=0)
    e_set = unv_read.read_sets(setn=1)
    node = convert_to_node(n_set)
    elem = convert_to_element(e_set)
    dataset = convert_to_dset(node, elem)

    unv_write = pyuff.UFF(copy_unv_file)
    unv_write.write_sets(dataset, mode='overwrite')
