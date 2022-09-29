import pandas as pd
from io import BytesIO

def to_excel(df, Sheet_Name):
    output = BytesIO()
    writer = pd.ExcelWriter(output)  #, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=Sheet_Name)
    workbook = writer.book
    worksheet = writer.sheets[Sheet_Name]
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def Ad_Copy_Builder(uploaded_file_data):

    if uploaded_file_data is not None:
        df = pd.read_excel(uploaded_file_data, sheet_name = 'Agent Info')
        ref1 = pd.read_excel('Ref - Ad Copy.xlsx', sheet_name = 'Headers')
        ref2 = pd.read_excel(uploaded_file_data, sheet_name = 'Ad Copy Template')

    ### -- Make Changes on DF ---
    df['Customer First Name'] = df['Agent Name'].str.split(' ',expand=True)[0]
    df['Row Type'] = 'Ad'
    df['Action'] = 'Create'
    df['Ad type'] = 'Responsive search'

    df['tmp'] = 1
    ref2['tmp'] = 1

    df = pd.merge(df, ref2, on=['tmp'])
    df = df.drop('tmp', axis=1)

    df.columns = df.columns.str.replace('Headline','Ad title')
    df.columns = df.columns.str.replace('Description Line','Ad description line')
    df.columns = df.columns.str.replace('Path','Ad path field')
    df.rename(columns = {'Final URL':'Ad landing page', 
                        'Ad Group':'Ad group', 
                        'Ad title 1':'Ad title'}, inplace = True)

    ### -- Fill Agent Name tokens on Ref File -- 
    def Agentname(x):
        
        for column in columns:
            if '[agentname]' in str(x[column].lower()):
                if column in ['Ad description line 1', 'Ad description line 2', 'Ad description line 3', 'Ad description line 4']:
                    if len(x[column]) + len(x['Agent Name']) - agentname_len > 90:
                        # Using agents' first name instead of full name to be able to stay under 90 characters
                        x[column] = x[column].replace('[agentname]', x['Customer First Name']) 
                    else:
                        x[column] = x[column].replace('[agentname]', x['Agent Name'])
                    
                elif column in ['Ad title', 'Ad title 2', 'Ad title 3', 'Ad title 4', 'Ad title 5', 'Ad title 6', 'Ad title 7', 'Ad title 8',
                'Ad title 9', 'Ad title 10', 'Ad title 11', 'Ad title 12', 'Ad title 13', 'Ad title 14', 'Ad title 15']:
                    if len(x[column]) + len(x['Agent Name']) - agentname_len > 30:
                        # Using agents' first name instead of full name to be able to stay under 30 characters
                        x[column] = x[column].replace('[agentname]', x['Customer First Name']) 
                    else:
                        x[column] = x[column].replace('[agentname]', x['Agent Name'])
                                            
                else:
                    x[column] = x[column].replace('[agentname]', x['Agent Name'])
        return x

    agentname_len = len('[agentname]')

    columns = df.columns

    Named_df = df.apply(Agentname, axis=1)


    def Final_URL(x):
        return x.replace('https:\/\/www\.URL\.com\/localagent', x['Agent Website'], regex=True)

    URL_df = Named_df.apply(Final_URL, axis=1)

    new_df = pd.concat([ref1, URL_df])
    return new_df