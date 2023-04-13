from io import StringIO
import pandas as pd
import requests
import time
from Bio import AlignIO
from Bio.Align import AlignInfo

file_names = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']
merged_data = pd.DataFrame()

for file in file_names:
    data = pd.read_excel(file, sheet_name=None, engine='openpyxl')
    for sheet, df in data.items():
        df['Species'] = sheet
        merged_data = pd.concat([merged_data, df], ignore_index=True)

grouped_data = merged_data.groupby('Signature')
signature_sequences = {}

for signature, group in grouped_data:
    signature_sequences[signature] = group['Protein Sequence'].tolist()


def clustal_omega_msa(sequences):
    base_url = 'https://www.ebi.ac.uk/Tools/services/rest/clustalo'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Submit the job
    params = {'sequence': '\n'.join(sequences), 'email': 'your@email.com'}
    response = requests.post(f'{base_url}/run', headers=headers, data=params)
    job_id = response.text

    # Check the job status
    while True:
        response = requests.get(f'{base_url}/status/{job_id}')
        status = response.text
        if status == 'RUNNING':
            time.sleep(10)
        elif status == 'FINISHED':
            break
        else:
            raise Exception(f'Clustal Omega job failed with status: {status}')

    # Retrieve the results
    response = requests.get(f'{base_url}/result/{job_id}/aln-fasta')
    return response.text

msa_results = {}

for signature, sequences in signature_sequences.items():
    msa_results[signature] = clustal_omega_msa(sequences)


def calculate_conservation_score(msa_result):
    alignment = AlignIO.read(StringIO(msa_result), "fasta")
    summary_align = AlignInfo.SummaryInfo(alignment)
    conservation_scores = summary_align.pos_specific_score_matrix()

    # Calculate the average conservation score
    total_score = 0
    num_positions = len(conservation_scores)
    for i in range(num_positions):
        total_score += max(conservation_scores[i].values())
    return total_score / num_positions

conservation_scores = pd.DataFrame(columns=['Signature', 'Conservation Score'])

for signature, msa_result in msa_results.items():
    conservation_score = calculate_conservation_score(msa_result)
    conservation_scores = conservation_scores.append({'Signature': signature, 'Conservation Score': conservation_score}, ignore_index=True)
