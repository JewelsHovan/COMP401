from typing import List
from collections import Counter
"""
A representation of a record ledger from fLPS2.0 software output

"""
class FLPS_record:

    def __init__(self, sequenceName, seq_length, bias_type, lps_num, start_index, end_index, residue_count, pvalue, signature):
        # initialize attributes
        self.sequenceName = sequenceName
        self.seq_length = seq_length
        self.bias_type = bias_type
        self.lps_num = lps_num
        self.start_index = start_index
        self.end_index = end_index
        self.residue_count = residue_count
        self.pvalue = pvalue
        self.signature = signature

    # override of str
    def __str__(self):
        return f"SeqName: {self.sequenceName}\tSeqLength: {self.seq_length}\tBiasType: {self.bias_type} Residue Count: {self.residue_count}\tSignature: {self.signature}\tIndex Range: [{self.start_index}, {self.end_index}]"
    
    # override of equals 
    def __eq__(self, other):
        return self.sequenceName == other.sequenceName and self.seq_length == other.seq_length and self.bias_type == other.bias_type and self.lps_num == other.lps_num and self.start_index == other.start_index and self.end_index == other.end_index and self.residue_count == other.residue_count and self.pvalue == other.pvalue and self.signature == other.signature

    # getters and setters
    def get_sequence_name(self):
        return self.sequenceName


class FLPS_ledger:
    """
    A representation of a record ledger from fLPS2.0 software output

    """
    def __init__(self, list_flps_records: List[FLPS_record] = []):
        # initialize attributes
        self.flps_records = list_flps_records
    
    def get_size(self):
        return len(self.flps_records)
    
    def add_record(self, record: FLPS_record):
        self.flps_records.append(record)
    
    def remove_record(self, del_record):
        if del_record.isinstancetype(FLPS_record):
            self.flps_records.remove(del_record)
        
    def find_records_by_name(self, record_name: str) -> List[FLPS_record]:
        records = []
        for record in self.flps_records:
            if record.get_sequence_name() == record_name:
                records.append(record)
        return records
    
    def get_sequence_names(self):
        return [record.get_sequence_name() for record in self.flps_records]
    
    def get_sequence_lengths(self):
        return [record.seq_length for record in self.flps_records]
    
    def get_bias_types(self):
        return [record.bias_type for record in self.flps_records]
    
    def get_lps_numbers(self):
        return [record.lps_num for record in self.flps_records]
    
    def get_index_ranges(self):
        return [(record.start_index, record.end_index) for record in self.flps_records]
    
    def get_p_values(self):
        return [record.pvalue for record in self.flps_records]
    
    def get_signatures(self):
        return [record.signature for record in self.flps_records]
    
    def get_residue_counts(self):
        return [record.residue_count for record in self.flps_records]
    

    def get_most_biased_regions(self):
        most_biased_regions = Counter(self.get_sequence_names())
        return most_biased_regions
    
    """
    Returns a list of information for the sequences with most disordered regions up to the range 
    """
    def get_information(self, range: int):
        biased_records = self.get_most_biased_regions().most_common(range)
        for record_count in biased_records:
            record_name = record_count[0]
            count = record_count[1]
            records_by_name = self.find_records_by_name(record_name) # list of FLPS objects with record name
            bias_counter = Counter([record.bias_type for record in records_by_name])
            residue_counter = Counter([record.residue_count for record in records_by_name])
            signature_counter = Counter([record.signature for record in records_by_name])
            print_str = f"For sequence: {record_name}, there are {count} compositionally biased regions\nBiases: {bias_counter.most_common()}\nSignatures: {signature_counter.most_common()}\nResidue Counts: {residue_counter.most_common()}\n"
            print(print_str)
    
    def count_bias(self):
        bias_counter = Counter(self.get_bias_types())
        return bias_counter.most_common()
    
    def count_signatures(self):
        signature_counter = Counter(self.get_signatures())
        return signature_counter.most_common()
    
    def count_residues(self, range: int = None):
        residue_counter = Counter(self.get_residue_counts())
        return residue_counter.most_common(range)



        

    