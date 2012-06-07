import GenomeManipulator as gm

manipulator = gm.GenomeManipulator('/Users/zaman/avida/avida-core/support/config/instset-transsmt.cfg')
print manipulator.sequence_to_genome('ab')
print manipulator.generate_all_mutants('ab')