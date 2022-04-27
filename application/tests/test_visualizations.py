import pytest
import visualizations as vis
import os


@pytest.mark.visuals
def test_get_truth_table():
    table, atoms = vis.get_truth_table('A & B & C')
    assert (
        'A' in atoms and 
        'B' in atoms and 
        'C' in atoms and 
        len(atoms) == 3
    )
    assert len(table) == 8  # 2**3
    for invals, outval in table:
        actual_outval = invals[0] and invals[1] and invals[2]
        assert actual_outval == bool(outval)


@pytest.mark.visuals
def test_draw_expression_tree():
    vis_filepath = vis.draw_expression_tree('A & B', view=False)
    for filepath in [vis_filepath, vis_filepath+'.pdf']:
        assert os.path.exists(filepath)
        os.remove(filepath)
    