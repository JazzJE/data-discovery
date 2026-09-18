from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("sagawa/ReactionT5v2-forward", return_tensors="pt")
model = AutoModelForSeq2SeqLM.from_pretrained("sagawa/ReactionT5v2-forward")

inp = tokenizer('REACTANT:COC(=O)C1=CCCN(C)C1.O.[Al+3].[H-].[Li+].[Na+].[OH-]REAGENT:C1CCOC1', return_tensors='pt')
output = model.generate(**inp, num_beams=1, num_return_sequences=1, return_dict_in_generate=True, output_scores=True)
output = tokenizer.decode(output['sequences'][0], skip_special_tokens=True).replace(' ', '').rstrip('.')
print(output) # 'CN1CCC=C(CO)C1'