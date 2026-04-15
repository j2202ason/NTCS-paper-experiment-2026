import pandas as pd
import ast,os
import pandas as pd
import json
import ast

class clsdataextractor:
    def __init__(self):
        pass

    def extract_solutions_to_xlsx(self, input_excel_path, output_excel_path):

        try:
            df = pd.read_excel(input_excel_path)
            print(f"success to read excel: {input_excel_path}")
            print(f"{len(df)} lines are found ")

            # 2. 检查solutions列是否存在
            if 'solutions' not in df.columns:
                # 检查是否有类似名称的列
                possible_columns = [col for col in df.columns if 'solution' in col.lower()]
                if possible_columns:
                    print(f"can not found column 'solutions',but found relative columns: {possible_columns}")
                    solution_column = possible_columns[0]
                else:
                    raise ValueError("there are no column 'solutions' in exdel")
            else:
                solution_column = 'solutions'

            print(f"get '{solution_column}' successfully")

            all_recommended_solutions = []

            # 3. 遍历每一行，提取"Recommended solutions"
            for idx, row in df.iterrows():
                solutions_str = row[solution_column]

                if pd.isna(solutions_str):
                    print(f"warining: the {idx}th line is empty，pass it")
                    continue

                try:
                    solutions_data = None

                    if isinstance(solutions_str, str):
                        try:
                            solutions_data = ast.literal_eval(solutions_str)
                        except (ValueError, SyntaxError):
                            try:
                                solutions_data = json.loads(solutions_str)
                            except json.JSONDecodeError:
                                if isinstance(solutions_str, dict):
                                    solutions_data = solutions_str
                                else:
                                    print(f"warning: the {idx}th line can not be parsed，pass it")
                                    continue

                    elif isinstance(solutions_str, dict):
                        solutions_data = solutions_str

                    if solutions_data and isinstance(solutions_data, dict):
                        if "Recommended solutions" in solutions_data:
                            recommended_list = solutions_data["Recommended solutions"]
                        elif "recommended solutions" in solutions_data:
                            recommended_list = solutions_data["recommended solutions"]
                        else:
                            recommended_keys = [key for key in solutions_data.keys()
                                                if isinstance(key, str) and "recommended" in key.lower()]

                            if recommended_keys:
                                recommended_list = solutions_data[recommended_keys[0]]
                            else:
                                print(f"Warning: the {idx}th line has no key named 'Recommended solutions'，pass")
                                continue

                        if isinstance(recommended_list, list):
                            all_recommended_solutions.extend(recommended_list)
                            print(f"the {idx}th line: get {len(recommended_list)} solutions")
                        else:
                            print(f"Warning: The 'Recommended solutions' of the {idx}th line is not a list，pass")
                    else:
                        print(f"Warning: the {idx}th line is not a dict, pass")

                except Exception as e:
                    print(f"an error in the {idx}th line: {e}")
                    continue

            if all_recommended_solutions:
                output_df = pd.DataFrame({"Recommended Solutions": all_recommended_solutions})

                output_df.to_excel(output_excel_path, index=False)

                print(f"\nsuccessfully write {len(all_recommended_solutions)} solutions to: {output_excel_path}")

                for i, solution in enumerate(all_recommended_solutions[:5]):
                    print(f"{i + 1}. {solution[:100]}..." if len(solution) > 100 else f"{i + 1}. {solution}")
            else:
                print("Warning: no recommended solutions are found")

        except FileNotFoundError:
            print(f"error:  {input_excel_path} are not found")
        except PermissionError:
            print(f"error: can't read {input_excel_path} or write to {output_excel_path}")
        except Exception as e:
            print(f"error: {e}")

    def extractor_main(self,finput,foutput):
        fp=os.getcwd()
        for i in range(0,5):
            #finput=os.path.join(fp,f"./data/exp_data_case{i}.xlsx")
            #foutput=os.path.join(fp,f"./data/recommended_solutions_case{i}.xlsx")
            self.extract_solutions_to_xlsx(finput,foutput)