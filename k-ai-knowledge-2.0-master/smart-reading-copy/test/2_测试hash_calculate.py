from indexing.hash_calculate import HashCalculate


hash_calculate = HashCalculate()
path = r'E:\python\k-ai-knowledge-2.0\smart-reading-copy\data\files\sample_document.pdf'
print(hash_calculate.compute_hash_from_file(path))
print(hash_calculate.compute_hash_from_file(path))
print(hash_calculate.compute_hash_from_file(path))