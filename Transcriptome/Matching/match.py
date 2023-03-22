# given a fasta file of the proteome and fasta file of the transciptome 
# match a protein sequences to corresponding cDNA transcript
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Seq import Seq

input_fasta_proteome = '/home/julienh/Desktop/COMP401/Proteomes/Drosophila/drosophila_7227.fasta'
input_fasta_transcript = '/home/julienh/Desktop/COMP401/Transcriptome/Drosophila/UP000000803_7227_DNA.fasta'

# Load the proteome and transcriptome files
proteome = SeqIO.to_dict(SeqIO.parse(input_fasta_proteome, "fasta"))
transcriptome = SeqIO.to_dict(SeqIO.parse(input_fasta_transcript, "fasta"))

# Define the protein sequence to search for
protein_sequence = "MPFPSLQECEQMVQMLRVVELQKILSFLNISFAGRKTDLQSRILSFLRTNLELLAPKVQEVYAQSVQEQNATLQYIDPTRMYSHIQLPPTVQPNPVGLVGSGQGVQVPGGQMNVVGGAPFLHTHSINSQLPIHPDVRLKKLAFYDVLGTLIKPSTLVPRNTQRVQEVPFYFTLTPQQATEIASNRDIRNSSKVEHAIQVQLRFCLVETSCDQEDCFPPNVNVKVNNKLCQLPNVIPTNRPNVEPKRPPRPVNVTSNVKLSPTVTNTITVQWCPDYTRSYCLAVYLVKKLTSTQLLQRMKTKGVKPADYTRGLIKEKLTEDADCEIATTMLKVSLNCPLGKMKMLLPCRASTCSHLQCFDASLYLQMNERKPTWNCPVCDKPAIYDNLVIDGYFQEVLGSSLLKSDDTEIQLHQDGSWSTPGLRSETQILDTPSKPAQKVEVISDDIELISDDAKPVKRDLSPAQDEQPTSTSNSETVDLTLSDSDDDMPLAKRRPPAKQAVASSTSNGSGGGQRAYTPAQQPQQSAVSAMNTMRKAK" 

# Create a Bio.Seq object from the protein sequence
protein_record = SeqIO.SeqRecord(Seq(protein_sequence), id="query")

# Perform the BLAST search
result_handle = NCBIWWW.qblast("tblastn", "nt", protein_record.seq)
blast_record = NCBIXML.read(result_handle)
print(blast_record)

# Get the top hit
hit = blast_record.alignments[0]
print(hit)

# Get the corresponding transcript sequence
transcript_id = hit.hit_id.split("|")[1]  # Extract the transcript ID from the hit ID
transcript_sequence = transcriptome[transcript_id].seq

# Print the transcript sequence
print(transcript_sequence)