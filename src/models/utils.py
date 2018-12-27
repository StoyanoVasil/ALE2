
def swap_node_shape(dot, node_id, new_shape):
    for i in range(len(dot.body)):
        if node_id in dot.body[i]:
            dot.body[i] = dot.body[i].replace('circle', new_shape)
