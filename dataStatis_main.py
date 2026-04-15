from extractData import clsdataextractor
from Clustor import *
import os
import visualizeData as vd

clt=None

def extractsolutions(i,fp,object):
    ficp=os.path.join(fp, "source")
    finput = os.path.join(ficp, f"exp_data_case{i}.xlsx")
    focp=os.path.join(fp, "extractor")
    foutput = os.path.join(focp, f"recommended_solutions_case{i}.xlsx")
    object.extract_solutions_to_xlsx(finput, foutput)

def mark_visualize(i,fp,tmcode):
    fip=os.path.join(fp, "extractor")
    input_file = os.path.join(fip, f"recommended_solutions_case{i}.xlsx")
    excel_path = input_file
    text_column = "Recommended Solutions"

    fop=os.path.join(fp, "cluster")
    output_path = os.path.join(fop, f"adaptive_clustering_results_case{i}.xlsx")

    dict_solution, dict_count = adaptive_text_clustering_from_excel(
        excel_path=excel_path,
        text_column=text_column,
        auto_cluster_method='silhouette',
        clustering_algorithm='kmeans',
        min_clusters=2,
        max_clusters=10,
        visualize=True
    )

    if dict_solution:
        output_data = []
        for cluster_desc, texts in dict_solution.items():
            for text in texts:
                output_data.append({
                    'Cluster_Description': cluster_desc,
                    'Original_Text': text,
                    'Text_Length': len(text),
                    'Cluster_Size': len(texts)
                })

    output_df = pd.DataFrame(output_data)
    output_df.to_excel(output_path, index=False)
    vd.visualdata(dict_count, i,fp,tmcode)

def statis(lstCase,curpath,tmcode):
    clt = clsdataextractor()
    fp=curpath
    for i in lstCase:
        extractsolutions(i,fp,clt)
        mark_visualize(i,fp,tmcode)
