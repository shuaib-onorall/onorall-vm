import pandas as pd
#Always create xlsx file using this code otherwise may be create some format issue
writer = pd.ExcelWriter('new-data.xlsx' , engine='xlsxwriter')
writer.save()
def d(name , company):
    dataframe1 = pd.read_excel('new-data.xlsx' , engine="openpyxl")
    df2 = pd.DataFrame({   'Serial' : [name  ] ,  'Company':[company] ,'Employee':['xbsxs'] , 'Discription':['sbsis']  ,  'Leave':['sbsis'  ]})
    new_data = pd.concat([dataframe1 , df2]   )
    result = pd.ExcelWriter('new-data.xlsx',  engine="openpyxl" )
    
    n_data =  new_data.to_excel( result  , sheet_name='new-data.xlsx'  , index=False)
    result.save()
    print(new_data)
    return True

d=d('JAI HIND' , '45')
